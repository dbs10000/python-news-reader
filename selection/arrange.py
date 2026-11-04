# ==========================================================================
# ARRANGE
# ------------------------------
# Gathers entries from the chosen sources, removes repeats, sorts them newest first,
# and limits how many come from each source.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports the re module for simplifying headlines when spotting repeats
import re
# Imports datetime tools for reading and comparing publish dates
from datetime import datetime, timezone

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser


# ------------------------------
# COLLECT FUNCTION
# ------------------------------
def collect_entries_from_sources(all_feeds: dict[str, feedparser.FeedParserDict],
                                 chosen_source_names: set[str]) -> list[feedparser.FeedParserDict]:
    """
    Gather every entry from the chosen sources into one list, labelled with its source.

    Parameters:
        all_feeds (dict[str, feedparser.FeedParserDict]): Source names mapped to their parsed feeds.
        chosen_source_names (set[str]): The names of the sources to include.

    Returns:
        list[feedparser.FeedParserDict]: Every entry, each with a "source_name" added.
    """
    collected_entries = []  # Stores every entry from every chosen source

    # Loop through each feed, skipping the ones that weren't chosen
    for source_name, parsed_feed in all_feeds.items():
        if source_name not in chosen_source_names:
            continue

        # Label each article with where it came from and add it to the list
        for entry in parsed_feed.entries:
            entry["source_name"] = source_name
            collected_entries.append(entry)

    return collected_entries


# ------------------------------
# DUPLICATE FUNCTIONS
# ------------------------------
def simplify_headline(headline: str) -> str:
    """
    Reduce a headline to lowercase letters and numbers only, so near-identical headlines match.

    Parameters:
        headline (str): A headline, e.g. "SK Hynix Shares Surge!"

    Returns:
        str: The simplified headline, e.g. "skhynixsharessurge"
    """
    return re.sub(r"[^a-z0-9]", "", headline.lower())  # Remove everything except letters and numbers


def remove_duplicate_entries(news_entries: list[feedparser.FeedParserDict]) -> list[feedparser.FeedParserDict]:
    """
    Remove entries that share a link or headline with an earlier entry.

    Parameters:
        news_entries (list[feedparser.FeedParserDict]): The entries to check.

    Returns:
        list[feedparser.FeedParserDict]: The entries with repeats removed; the first copy is kept.
    """
    seen_links = set()  # Links already kept
    seen_headlines = set()  # Simplified headlines already kept
    unique_entries = []  # Stores entries that aren't repeats

    for entry in news_entries:
        entry_link = entry.get("link", "")
        simple_headline = simplify_headline(entry.get("title", ""))

        # Skip this entry if its link or headline has been seen before
        if (entry_link and entry_link in seen_links) or (simple_headline and simple_headline in seen_headlines):
            continue

        seen_links.add(entry_link)  # Remember this link
        seen_headlines.add(simple_headline)  # Remember this headline
        unique_entries.append(entry)

    return unique_entries


# ------------------------------
# DATE FUNCTIONS
# ------------------------------
def get_entry_datetime(entry: feedparser.FeedParserDict) -> datetime | None:
    """
    Get when an entry was published (or updated, if no publish date is given).

    Parameters:
        entry (feedparser.FeedParserDict): A single news entry.

    Returns:
        datetime | None: The date and time in UTC, or None if the entry has no date.
    """
    # feedparser stores dates it understood as "_parsed" values, already converted to UTC
    parsed_date = entry.get("published_parsed") or entry.get("updated_parsed")

    if parsed_date is None:
        return None

    # The first six parts are year, month, day, hour, minute and second
    return datetime(*parsed_date[:6], tzinfo=timezone.utc)


def sort_entries_newest_first(news_entries: list[feedparser.FeedParserDict]) -> list[feedparser.FeedParserDict]:
    """
    Sort entries so the most recent come first. Entries without a date go to the end.

    Parameters:
        news_entries (list[feedparser.FeedParserDict]): The entries to sort.

    Returns:
        list[feedparser.FeedParserDict]: A new, sorted list.
    """
    oldest_possible_date = datetime.min.replace(tzinfo=timezone.utc)  # Used for entries with no date

    def get_sort_date(entry: feedparser.FeedParserDict) -> datetime:
        """Return the entry's date, or the oldest possible date if it has none."""
        return get_entry_datetime(entry) or oldest_possible_date

    return sorted(news_entries, key=get_sort_date, reverse=True)  # reverse=True puts newest first


# ------------------------------
# LIMIT FUNCTION
# ------------------------------
def limit_entries_per_source(news_entries: list[feedparser.FeedParserDict],
                             entries_per_source: int) -> list[feedparser.FeedParserDict]:
    """
    Keep only the first few entries from each source, in the order given.

    Parameters:
        news_entries (list[feedparser.FeedParserDict]): Entries labelled with "source_name".
        entries_per_source (int): How many to keep from each source. 0 keeps them all.

    Returns:
        list[feedparser.FeedParserDict]: The limited entries, still in the order given.
    """
    # 0 means no limit
    if entries_per_source == 0:
        return list(news_entries)

    kept_count_by_source = {}  # How many entries have been kept from each source so far
    limited_entries = []  # Stores the entries that fit within the limit

    for entry in news_entries:
        source_name = entry.get("source_name", "")
        kept_count = kept_count_by_source.get(source_name, 0)  # 0 if none kept from this source yet

        # Keep the entry only if this source hasn't reached its limit
        if kept_count < entries_per_source:
            limited_entries.append(entry)
            kept_count_by_source[source_name] = kept_count + 1

    return limited_entries
