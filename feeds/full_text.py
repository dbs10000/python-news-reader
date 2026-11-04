# ==========================================================================
# FULL TEXT
# ------------------------------
# Fetches the full text of an article from its web page, because feeds (especially Google Alerts)
# only include a short snippet.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports lru_cache, which remembers results so the same article is only downloaded once
from functools import lru_cache

# External Modules
# ------------------------------
# Imports trafilatura, which downloads a web page and pulls out just the article text
import trafilatura


# ------------------------------
# FULL TEXT FUNCTION
# ------------------------------
@lru_cache(maxsize=200)  # Remember the last 200 articles fetched
def fetch_full_article_text(article_link: str) -> str | None:
    """
    Download an article's web page and return just its main text, without menus or adverts.

    Parameters:
        article_link (str): The article's web address.

    Returns:
        str | None: The article text, with paragraphs separated by new lines,
            or None if the page couldn't be downloaded or had no readable text
            (often because it's paywalled or blocks automatic readers).
    """
    # Nothing to fetch without a link
    if not article_link:
        return None

    downloaded_page = trafilatura.fetch_url(article_link)  # Download the page's HTML

    # Stop if the site refused or the download failed
    if downloaded_page is None:
        return None

    # Pull out the main article text, leaving out comments and tables
    return trafilatura.extract(
        downloaded_page,
        include_comments=False,
        include_tables=False,
        favor_precision=True,  # Prefer leaving a bit out over including menus and adverts
    )
