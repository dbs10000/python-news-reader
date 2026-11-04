# ==========================================================================
# FORMATTING
# ------------------------------
# Turns raw entry data into friendly text for the screen: "3 h ago", "bbc.co.uk", highlighted matches.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports the html module for making text safe to show as HTML
import html
# Imports the re module for finding search terms to highlight
import re
# Imports datetime tools for working out how long ago something was published
from datetime import datetime, timezone
# Imports urlparse for pulling the website name out of a link
from urllib.parse import urlparse


# ------------------------------
# TEXT FUNCTIONS
# ------------------------------
def get_publisher_name(article_link: str) -> str:
    """
    Get the website name from an article link.

    Parameters:
        article_link (str): e.g. "https://www.theguardian.com/uk/2026/..."

    Returns:
        str: The website name, e.g. "theguardian.com", or "" if there's no link.
    """
    website_address = urlparse(article_link).netloc  # The part between "https://" and the next "/"
    return website_address.removeprefix("www.")  # "www." adds nothing, so drop it


def format_time_ago(published_datetime: datetime | None) -> str:
    """
    Describe how long ago something was published, the way people say it.

    Parameters:
        published_datetime (datetime | None): When it was published, in UTC.

    Returns:
        str: e.g. "just now", "12 min ago", "3 h ago", "yesterday", "28 Oct". "" if there's no date.
    """
    if published_datetime is None:
        return ""

    seconds_ago = (datetime.now(timezone.utc) - published_datetime).total_seconds()  # Age in seconds

    if seconds_ago < 60:
        return "just now"
    if seconds_ago < 60 * 60:
        return f"{int(seconds_ago // 60)} min ago"
    if seconds_ago < 24 * 60 * 60:
        return f"{int(seconds_ago // 3600)} h ago"
    if seconds_ago < 48 * 60 * 60:
        return "yesterday"
    return f"{published_datetime.day} {published_datetime:%b}"  # e.g. "28 Oct"


def format_exact_date(published_datetime: datetime | None) -> str:
    """
    Write out the exact publish date and time.

    Parameters:
        published_datetime (datetime | None): When it was published, in UTC.

    Returns:
        str: e.g. "Sun 1 Nov 2026, 14:05 UTC", or "Date not given".
    """
    if published_datetime is None:
        return "Date not given"

    return f"{published_datetime:%a} {published_datetime.day} {published_datetime:%b %Y, %H:%M} UTC"


def is_recently_published(published_datetime: datetime | None, within_hours: float) -> bool:
    """
    Check whether something was published within the last few hours.

    Parameters:
        published_datetime (datetime | None): When it was published, in UTC.
        within_hours (float): How many hours count as recent.

    Returns:
        bool: True if it was published within that many hours; False if older or undated.
    """
    if published_datetime is None:
        return False

    hours_ago = (datetime.now(timezone.utc) - published_datetime).total_seconds() / 3600
    return hours_ago <= within_hours


def highlight_search_terms(plain_text: str, search_terms: list[str]) -> str:
    """
    Make text safe to show as HTML and wrap each search term in <mark> tags so it's highlighted.

    Parameters:
        plain_text (str): The text to show, e.g. "Oil prices fall"
        search_terms (list[str]): The terms to highlight, e.g. ["oil"]

    Returns:
        str: HTML, e.g. "<mark>Oil</mark> prices fall"
    """
    safe_text = html.escape(plain_text)  # Turn < > & into safe codes so feed text can't break the page

    if not search_terms:
        return safe_text

    # Longest terms first, so "oil price" is highlighted as a whole before "oil" is tried
    terms_longest_first = sorted(search_terms, key=len, reverse=True)

    # One pattern that matches any of the terms as whole words, e.g. \b(oil price|oil)\b
    escaped_terms = [re.escape(html.escape(search_term)) for search_term in terms_longest_first]
    any_term_pattern = r"\b(" + "|".join(escaped_terms) + r")\b"

    # \1 puts back whatever was matched, keeping its original upper or lower case
    return re.sub(any_term_pattern, r"<mark>\1</mark>", safe_text, flags=re.IGNORECASE)
