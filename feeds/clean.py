# ==========================================================================
# CLEAN
# ------------------------------
# Tidies up Google Alerts entries: removes HTML, fixes special characters, and swaps in real links.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports the html module for converting HTML codes like &#39; into normal characters
import html
# Imports the re module for finding and removing HTML tags
import re
# Imports urlparse and parse_qs for pulling the real link out of Google's redirect links
from urllib.parse import urlparse, parse_qs

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser


# ------------------------------
# CLEANUP FUNCTIONS
# ------------------------------
def clean_html_text(html_text: str) -> str:
    """
    Remove HTML tags and convert HTML codes into normal characters.

    Parameters:
        html_text (str): Text containing HTML, e.g. "Global <b>shortage</b> isn&#39;t<br>over"

    Returns:
        str: Plain text, e.g. "Global shortage isn't over"
    """
    text_with_spaces = re.sub(r"<br\s*/?>", " ", html_text, flags=re.IGNORECASE)  # Turn line breaks into spaces
    text_without_tags = re.sub(r"<[^>]+>", "", text_with_spaces)  # Remove all other tags, like <b>
    single_spaced_text = re.sub(r"\s+", " ", text_without_tags).strip()  # Squash repeated spaces into one
    return html.unescape(single_spaced_text)  # Turn codes like &#39; into '


def get_real_article_link(google_redirect_link: str) -> str:
    """
    Extract the real article link from a Google redirect link.

    Parameters:
        google_redirect_link (str): A link starting with https://www.google.com/url?...

    Returns:
        str: The real article link, or the original link if no real link is found.
    """
    link_query = urlparse(google_redirect_link).query  # Get the part of the link after the ?
    query_values = parse_qs(link_query)  # Split it into a dictionary of names and values
    return query_values.get("url", [google_redirect_link])[0]  # Return the 'url' value if it exists


def clean_google_alert_feeds(parsed_google_alert_feeds: dict[str, feedparser.FeedParserDict]) -> None:
    """
    Clean the titles, summaries and links of every entry in each Google Alerts feed.

    Parameters:
        parsed_google_alert_feeds (dict[str, feedparser.FeedParserDict]): Source names
            mapped to their parsed Google Alerts feeds.

    Returns:
        None: The entries are updated in place.
    """
    # Loop through each parsed Google Alerts feed
    for parsed_feed in parsed_google_alert_feeds.values():
        # Loop through each article in the feed
        for entry in parsed_feed.entries:
            entry["title"] = clean_html_text(entry.get("title", ""))  # Clean the headline
            entry["summary"] = clean_html_text(entry.get("summary", ""))  # Clean the summary
            entry["link"] = get_real_article_link(entry.get("link", ""))  # Swap in the real link
