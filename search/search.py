# ==========================================================================
# SEARCH
# ------------------------------
# Filters entries down to the ones that mention the search terms.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports the re module for whole-word searching
import re

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser


# ------------------------------
# SEARCH FUNCTIONS
# ------------------------------
def split_search_text(search_text: str) -> list[str]:
    """
    Turn what the user typed in the search box, like "Nvidia, oil", into a list of terms.

    Parameters:
        search_text (str): The text in the search box.

    Returns:
        list[str]: The search terms in lowercase, e.g. ["nvidia", "oil"]. Empty if nothing was typed.
    """
    search_terms = []  # Stores each search term

    # Split the text at each comma and tidy up each term
    for typed_term in search_text.split(","):
        cleaned_term = typed_term.strip().lower()  # Remove spaces and make lowercase

        # Skip empty terms, e.g. from a trailing comma
        if cleaned_term:
            search_terms.append(cleaned_term)

    return search_terms


def entry_contains_term(entry: feedparser.FeedParserDict, search_term: str) -> bool:
    """
    Check whether an entry's headline or summary contains a search term as a whole word.

    Parameters:
        entry (feedparser.FeedParserDict): A single news entry.
        search_term (str): The word or phrase to look for.

    Returns:
        bool: True if the term is found, otherwise False.
    """
    searchable_text = entry.get("title", "") + " " + entry.get("summary", "")  # Join headline and summary

    # \b marks a word edge, so "oil" matches "oil" but not "soil" or "boiling".
    # re.escape stops symbols in the term (like "." or "+") being treated as special pattern codes.
    whole_word_pattern = rf"\b{re.escape(search_term)}\b"

    # Search the text, ignoring upper and lower case; returns True if found
    return re.search(whole_word_pattern, searchable_text, re.IGNORECASE) is not None


def entry_matches_search(entry: feedparser.FeedParserDict, search_terms: list[str], match_all_terms: bool) -> bool:
    """
    Check whether an entry matches the search.

    Parameters:
        entry (feedparser.FeedParserDict): A single news entry.
        search_terms (list[str]): The terms to look for.
        match_all_terms (bool): True to require every term; False to accept any one of them.

    Returns:
        bool: True if the entry matches.
    """
    # Check each term separately, giving a list like [True, False]
    terms_found = [entry_contains_term(entry, search_term) for search_term in search_terms]

    # all() is True only if every term was found; any() is True if at least one was
    return all(terms_found) if match_all_terms else any(terms_found)


def filter_entries_by_search(news_entries: list[feedparser.FeedParserDict],
                             search_terms: list[str],
                             match_all_terms: bool) -> list[feedparser.FeedParserDict]:
    """
    Keep only the entries that match the search. With no search terms, every entry is kept.

    Parameters:
        news_entries (list[feedparser.FeedParserDict]): The entries to search through.
        search_terms (list[str]): The terms to look for.
        match_all_terms (bool): True to require every term; False to accept any one of them.

    Returns:
        list[feedparser.FeedParserDict]: The matching entries, in the same order.
    """
    # No search means nothing to filter out
    if not search_terms:
        return list(news_entries)

    matching_entries = []  # Stores entries that match

    for entry in news_entries:
        if entry_matches_search(entry, search_terms, match_all_terms):
            matching_entries.append(entry)

    return matching_entries
