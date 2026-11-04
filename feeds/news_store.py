# ==========================================================================
# NEWS STORE
# ------------------------------
# Keeps the latest downloaded news in one place, so every window or website visitor shares it
# instead of downloading everything again.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports datetime tools for remembering when the news was last downloaded
from datetime import datetime, timedelta, timezone

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser

# Project Modules
# ------------------------------
# Imports the news sources
from settings.feeds import FEEDS
# Imports the function that downloads, parses and cleans every feed
from feeds.fetch import load_all_feeds


# ------------------------------
# NEWS STORE CLASS
# ------------------------------
# A class bundles data and the functions that work on it. Here the data is the latest news,
# and the functions download it again and check whether it's out of date.
class NewsStore:
    """
    Holds the latest news and when it was downloaded.

    Attributes:
        news_sources (dict[str, str]): Source names mapped to their feed URLs.
        all_feeds (dict[str, feedparser.FeedParserDict]): Source names mapped to their parsed feeds.
        failed_source_names (list[str]): Sources that couldn't be read last time.
        last_updated (datetime | None): When the news was downloaded, or None if not yet.
    """

    def __init__(self, news_sources: dict[str, str]) -> None:
        """
        Create an empty news store.

        Parameters:
            news_sources (dict[str, str]): Source names mapped to their feed URLs.

        Returns:
            None
        """
        self.news_sources = news_sources  # The feeds to download
        self.all_feeds: dict[str, feedparser.FeedParserDict] = {}  # No news until the first download
        self.failed_source_names: list[str] = []  # No failures yet
        self.last_updated: datetime | None = None  # Not downloaded yet

    def refresh(self) -> None:
        """
        Download every feed again and remember when it happened. This can take a few seconds.

        Returns:
            None: The store's news is replaced with the fresh download.
        """
        self.all_feeds, self.failed_source_names = load_all_feeds(self.news_sources)
        self.last_updated = datetime.now(timezone.utc)  # Record the time in UTC so it's never ambiguous

    def is_out_of_date(self, max_age_minutes: int) -> bool:
        """
        Check whether the news needs downloading again.

        Parameters:
            max_age_minutes (int): How old the news may be before it counts as out of date.

        Returns:
            bool: True if the news has never been downloaded or is older than max_age_minutes.
        """
        if self.last_updated is None:
            return True

        news_age = datetime.now(timezone.utc) - self.last_updated  # How long ago it was downloaded
        return news_age > timedelta(minutes=max_age_minutes)


# ------------------------------
# SHARED NEWS STORE
# ------------------------------
# The one store the whole app uses: from feeds.news_store import news_store
news_store = NewsStore(FEEDS)
