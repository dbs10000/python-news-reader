# ==========================================================================
# EXPLORE FEED KEYS
# ------------------------------
# A helper tool, separate from the main programme. Run it when adding a new news source to see
# every piece of information (key) its entries contain, and an example of each.
# Run it with:  python explore_feed_keys.py
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser
# Imports escape, which stops text like "[Reuters]" being read as rich colour codes
from rich.markup import escape
# Imports Table, which draws neat rows and columns
from rich.table import Table
# Imports Console, which prints colours and tables
from rich.console import Console

# Project Modules
# ------------------------------
# Imports the news sources
from settings.feeds import FEEDS
# Imports the list of keys the programme treats as useful
from settings.entry_details import USEFUL_ENTRY_KEYS
# Imports the function that downloads, parses and cleans every feed
from feeds.fetch import load_all_feeds
# Imports the function that lists every key in a feed
from feeds.details import find_entry_keys


# ------------------------------
# CONSOLE
# ------------------------------
console = Console()  # Prints in colour to the terminal


# ------------------------------
# EXPLORE FUNCTIONS
# ------------------------------
def find_example_value(parsed_feed: feedparser.FeedParserDict, entry_key: str) -> str:
    """
    Find an example value for a key from the first entry that has it.

    Parameters:
        parsed_feed (feedparser.FeedParserDict): A parsed feed.
        entry_key (str): The key to find an example of.

    Returns:
        str: The example, shortened to 80 characters.
    """
    # Return the value from the first entry that has this key
    for entry in parsed_feed.entries:
        if entry_key in entry:
            example_text = str(entry[entry_key])  # Turn any kind of value into text
            return example_text[:80] + ("..." if len(example_text) > 80 else "")  # Shorten long examples

    return ""


def print_feed_keys_table(source_name: str, parsed_feed: feedparser.FeedParserDict) -> None:
    """
    Print a table of every key in a feed, whether it's used by the programme, and an example.

    Parameters:
        source_name (str): The name of the news source.
        parsed_feed (feedparser.FeedParserDict): The parsed feed.

    Returns:
        None: The table is printed to the output.
    """
    keys_table = Table(title=f"{escape(source_name)} ({len(parsed_feed.entries)} entries)", title_style="bold")
    keys_table.add_column("Key", style="cyan")  # The raw feedparser key
    keys_table.add_column("Used as")  # The friendly label, if the programme uses it
    keys_table.add_column("Example", overflow="fold")  # A sample value

    # Add one row per key found in the feed
    for entry_key in find_entry_keys(parsed_feed):
        used_as_label = USEFUL_ENTRY_KEYS.get(entry_key, "[dim]not used[/dim]")  # Label, or "not used"
        keys_table.add_row(entry_key, used_as_label, escape(find_example_value(parsed_feed, entry_key)))

    console.print(keys_table)


# ------------------------------
# RUN TOOL
# ------------------------------
# Only run this code when the script is run directly, not when it's imported
if __name__ == "__main__":
    all_feeds, failed_source_names = load_all_feeds(FEEDS)  # Download, parse and clean every feed

    # Print a keys table for each feed
    for source_name, parsed_feed in all_feeds.items():
        print_feed_keys_table(source_name, parsed_feed)

    # List any feeds that couldn't be read
    for source_name in failed_source_names:
        console.print(f"[red]Could not read feed: {escape(source_name)}[/red]")
