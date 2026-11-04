# ==========================================================================
# FEEDS
# ------------------------------
# The news sources the app reads, in groups. The groups become the headings in the sidebar.
# This is the only file you need to edit to make the app your own.
#
# HOW TO ADD YOUR OWN FEED
#   1. Find an RSS feed URL (see docs/ADDING_FEEDS.md for where to find them, including Google Alerts).
#   2. Replace a PLACEHOLDER_URL below with it, in quotes, and give the source a name:
#          "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
#   3. Restart the app.
#
# Rules:
#   - Every source name must be different.
#   - A source whose URL is still PLACEHOLDER_URL is shown in the sidebar as "not set up"
#     and is skipped, so the app runs fine before you've added anything.
#   - A URL can also be a file path, like the sample feeds below, which are stored in sample_feeds/.
# ==========================================================================

# ------------------------------
# PLACEHOLDER
# ------------------------------
# Any source whose URL is exactly this is treated as "not set up yet"
PLACEHOLDER_URL = "PASTE_YOUR_FEED_URL_HERE"


# ------------------------------
# FEED GROUPS DICT
# ------------------------------
# Group names mapped to their sources, and each source name mapped to its feed URL.
FEED_GROUPS = {
    # Your feeds
    # ---------------------------------
    # Rename these and paste in your own feed URLs. Add as many as you like.
    "My feeds": {
        "My first feed": PLACEHOLDER_URL,
        "My second feed": PLACEHOLDER_URL,
    },

    # Sample feeds
    # ---------------------------------
    # Made-up stories stored in sample_feeds/, so you can see the app working straight away.
    # Delete this group once you've added your own feeds.
    "Sample feeds (delete me)": {
        "Sample: Technology": "sample_feeds/technology.xml",
        "Sample: Science": "sample_feeds/science.xml",
        "Sample: Business": "sample_feeds/business.xml",
    },
}


# ------------------------------
# ALL FEEDS DICT
# ------------------------------
# Every source in one dictionary, built automatically from the groups above (no need to edit this).
FEEDS = {}  # Stores every source name mapped to its feed URL

# Copy the sources out of each group into the one dictionary
for group_feeds in FEED_GROUPS.values():
    FEEDS.update(group_feeds)
