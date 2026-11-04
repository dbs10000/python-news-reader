# ==========================================================================
# FETCH
# ------------------------------
# Downloads and parses the feeds, cleans Google Alerts ones, and returns them all together.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports ThreadPoolExecutor, which downloads several feeds at the same time instead of one by one
from concurrent.futures import ThreadPoolExecutor
# Imports Path, for finding feed files stored in the project folder
from pathlib import Path

# External Modules
# ------------------------------
# Imports the feedparser module for reading the news
import feedparser

# Project Modules
# ------------------------------
# Imports the cleanup step for Google Alerts feeds
from feeds.clean import clean_google_alert_feeds
# Imports the placeholder that marks a source as "not set up yet"
from settings.feeds import PLACEHOLDER_URL


# ------------------------------
# SETTINGS
# ------------------------------
# How many feeds to download at the same time
SIMULTANEOUS_DOWNLOADS = 8

# The project's main folder (one level up from this file), used to find feed files like the samples
PROJECT_FOLDER = Path(__file__).parent.parent


# ------------------------------
# FETCH FUNCTIONS
# ------------------------------
def split_feeds_by_type(news_sources: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    """
    Split news sources into standard feeds and Google Alerts feeds.

    Parameters:
        news_sources (dict[str, str]): Source names mapped to their feed URLs.

    Returns:
        tuple[dict[str, str], dict[str, str]]: Two dictionaries in the form
            (standard_feeds, google_alert_feeds), each mapping source names to URLs.
    """
    standard_feeds = {}  # Stores feeds that need no extra cleaning
    google_alert_feeds = {}  # Stores Google Alerts feeds that need cleaning

    # Loop through each source name and its feed URL
    for source_name, feed_url in news_sources.items():
        # Google Alerts feed URLs always contain this text
        if "google.com/alerts" in feed_url:
            google_alert_feeds[source_name] = feed_url  # Add to the Google Alerts group
        else:
            standard_feeds[source_name] = feed_url  # Add to the standard group

    return standard_feeds, google_alert_feeds


def is_feed_set_up(feed_url: str) -> bool:
    """
    Check whether a source has been given a real feed URL or file, rather than the placeholder.

    Parameters:
        feed_url (str): The URL from settings/feeds.py.

    Returns:
        bool: True if it's set up; False if it's empty or still the placeholder.
    """
    return bool(feed_url.strip()) and feed_url != PLACEHOLDER_URL


def find_set_up_feeds(news_sources: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """
    Separate the sources that have a feed URL from the ones still waiting for one.

    Parameters:
        news_sources (dict[str, str]): Source names mapped to their feed URLs.

    Returns:
        tuple[dict[str, str], list[str]]: In the form (set_up_feeds, not_set_up_source_names).
    """
    set_up_feeds = {}  # Stores sources that have a real URL
    not_set_up_source_names = []  # Stores the names of sources still using the placeholder

    for source_name, feed_url in news_sources.items():
        if is_feed_set_up(feed_url):
            set_up_feeds[source_name] = feed_url
        else:
            not_set_up_source_names.append(source_name)

    return set_up_feeds, not_set_up_source_names


def resolve_feed_location(feed_url: str) -> str:
    """
    Turn a file path like "sample_feeds/technology.xml" into a full path; leave web addresses alone.

    Parameters:
        feed_url (str): A web address or a file path relative to the project folder.

    Returns:
        str: Something feedparser can open: the web address, or the full file path.
    """
    if feed_url.startswith(("http://", "https://")):
        return feed_url

    return str(PROJECT_FOLDER / feed_url)  # The / joins folder and file names into one path


def parse_news_feeds(news_sources: dict[str, str]) -> tuple[dict[str, feedparser.FeedParserDict], list[str]]:
    """
    Download and parse the RSS feed for each news source, several at a time.

    Parameters:
        news_sources (dict[str, str]): Source names mapped to their feed URLs.

    Returns:
        tuple[dict[str, feedparser.FeedParserDict], list[str]]: In the form
            (parsed_feeds, failed_source_names). Sources that could not be read are
            left out of parsed_feeds and listed in failed_source_names instead.
    """
    # Turn any file paths (like the sample feeds) into full paths feedparser can open
    feed_locations = [resolve_feed_location(feed_url) for feed_url in news_sources.values()]

    # Download every feed at the same time; map keeps the results in the same order as the URLs
    with ThreadPoolExecutor(max_workers=SIMULTANEOUS_DOWNLOADS) as download_pool:
        parsed_feed_list = list(download_pool.map(feedparser.parse, feed_locations))

    parsed_feeds = {}  # Stores each successfully parsed feed by source name
    failed_source_names = []  # Stores the names of feeds that could not be read

    # Pair each source name with its parsed feed (zip walks through both lists side by side)
    for source_name, parsed_feed in zip(news_sources, parsed_feed_list):
        # 'bozo' is set when the feed had a problem; count it as failed if no articles came back
        if parsed_feed.bozo and not parsed_feed.entries:
            failed_source_names.append(source_name)
            continue

        parsed_feeds[source_name] = parsed_feed  # Save the parsed feed under its source name

    return parsed_feeds, failed_source_names


def load_all_feeds(news_sources: dict[str, str]) -> tuple[dict[str, feedparser.FeedParserDict], list[str]]:
    """
    Download, parse and clean every feed that's set up, keeping the order they were listed in.
    Sources still using the placeholder URL are skipped.

    Parameters:
        news_sources (dict[str, str]): Source names mapped to their feed URLs.

    Returns:
        tuple[dict[str, feedparser.FeedParserDict], list[str]]: In the form
            (all_feeds, failed_source_names).
    """
    set_up_feeds, _ = find_set_up_feeds(news_sources)  # Skip sources that are still placeholders
    parsed_feeds, failed_source_names = parse_news_feeds(set_up_feeds)  # Download everything at once

    # Clean only the Google Alerts feeds
    _, google_alert_feeds = split_feeds_by_type(news_sources)  # _ means "not needed here"
    parsed_google_alert_feeds = {}  # Stores the parsed Google Alerts feeds
    for source_name in google_alert_feeds:
        if source_name in parsed_feeds:
            parsed_google_alert_feeds[source_name] = parsed_feeds[source_name]
    clean_google_alert_feeds(parsed_google_alert_feeds)

    return parsed_feeds, failed_source_names
