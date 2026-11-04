# ==========================================================================
# DETAILS
# ------------------------------
# Finds which keys (pieces of information) each feed's entries have, and reads them as plain text.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser

# Project Modules
# ------------------------------
# Imports the list of keys the programme treats as useful
from settings.entry_details import USEFUL_ENTRY_KEYS
# Imports the HTML cleaner, so every detail comes back as plain text
from feeds.clean import clean_html_text


# ------------------------------
# KEY DISCOVERY FUNCTIONS
# ------------------------------
def find_entry_keys(parsed_feed: feedparser.FeedParserDict) -> list[str]:
    """
    List every key that appears in at least one entry of a feed.

    Parameters:
        parsed_feed (feedparser.FeedParserDict): A parsed feed.

    Returns:
        list[str]: Every key found, in alphabetical order, e.g. ["id", "link", "summary", "title"]
    """
    entry_keys = set()  # A set ignores repeats, so each key is only stored once

    # Add the keys from every entry in the feed
    for entry in parsed_feed.entries:
        entry_keys.update(entry.keys())

    return sorted(entry_keys)  # Turn the set into an alphabetical list


def find_useful_keys(entry_keys: list[str]) -> list[str]:
    """
    Pick out the keys that are listed as useful in settings, in the settings order.

    Parameters:
        entry_keys (list[str]): Every key found in a feed.

    Returns:
        list[str]: Only the useful keys, e.g. ["title", "summary", "link"]
    """
    useful_keys = []  # Stores the useful keys this feed has

    # Go through the useful keys in settings order and keep the ones this feed has
    for useful_key in USEFUL_ENTRY_KEYS:
        if useful_key in entry_keys:
            useful_keys.append(useful_key)

    return useful_keys


def find_useful_keys_for_feeds(parsed_feeds: dict[str, feedparser.FeedParserDict]) -> dict[str, list[str]]:
    """
    Find the useful keys available in each feed.

    Parameters:
        parsed_feeds (dict[str, feedparser.FeedParserDict]): Source names mapped to
            their parsed feeds.

    Returns:
        dict[str, list[str]]: Source names mapped to their useful keys.
    """
    useful_keys_by_feed = {}  # Stores each source name and its useful keys

    # Find the useful keys for each feed
    for source_name, parsed_feed in parsed_feeds.items():
        entry_keys = find_entry_keys(parsed_feed)  # Every key in this feed
        useful_keys_by_feed[source_name] = find_useful_keys(entry_keys)  # Only the useful ones

    return useful_keys_by_feed


def combine_useful_keys(useful_keys_by_feed: dict[str, list[str]]) -> list[str]:
    """
    Combine the useful keys from several feeds into one list, without repeats.

    Parameters:
        useful_keys_by_feed (dict[str, list[str]]): Source names mapped to their useful keys.

    Returns:
        list[str]: Every useful key found in any of the feeds, in settings order.
    """
    all_found_keys = []  # Stores every key found in any feed

    # Gather the keys from every feed
    for useful_keys in useful_keys_by_feed.values():
        all_found_keys.extend(useful_keys)

    return find_useful_keys(all_found_keys)  # Re-use the settings order and drop repeats


# ------------------------------
# DETAIL READING FUNCTION
# ------------------------------
def get_entry_detail(entry: feedparser.FeedParserDict, entry_key: str) -> str:
    """
    Read one detail from an entry as plain text, whatever shape feedparser stored it in.

    Parameters:
        entry (feedparser.FeedParserDict): A single news entry.
        entry_key (str): The key to read, e.g. "title" or "content"

    Returns:
        str: The detail as plain text, or "Not available" if the entry doesn't have it.
    """
    detail_value = entry.get(entry_key)  # Get the raw value, or None if it's missing

    # Stop early if the entry doesn't have this detail
    if not detail_value:
        return "Not available"

    # Some keys are stored as lists of dictionaries, so pull out the useful part
    if entry_key == "content":
        detail_value = detail_value[0].get("value", "")  # The text of the first content block
    elif entry_key == "tags":
        tag_names = []  # Stores the name of each tag
        for tag in detail_value:
            tag_names.append(tag.get("term", ""))  # Each tag's name is stored under "term"
        detail_value = ", ".join(tag_names)  # Join them into one line
    elif entry_key == "media_thumbnail":
        detail_value = detail_value[0].get("url", "")  # The image link of the first thumbnail

    plain_text = clean_html_text(str(detail_value))  # Remove any HTML left in the text
    return plain_text or "Not available"  # Fall back if cleaning left nothing behind
