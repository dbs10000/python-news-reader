# ==========================================================================
# NEWS LIST
# ------------------------------
# The main area: the list of articles, in whichever view the reader chose,
# plus friendly messages when there's nothing to show.
# Class names starting "news-" are hooks for the themes in gui/themes.py to style.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports Callable, the type for "a function passed in as a value"
from collections.abc import Callable

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser
# Imports NiceGUI's ui, which creates everything on screen
from nicegui import ui

# Project Modules
# ------------------------------
# Imports the reader's choices
from gui.reader_state import ReaderState
# Imports the helpers that turn entry data into friendly text
from gui.formatting import (
    format_exact_date, format_time_ago, get_publisher_name, highlight_search_terms, is_recently_published,
)
# Imports the function that opens an article's original page
from gui.links import open_original_article
# Imports the functions that read dates and split the search box text
from selection.arrange import get_entry_datetime
from search.search import split_search_text
# Imports the feed list and the check for whether a source has a real feed URL yet
from settings.feeds import FEEDS
from feeds.fetch import is_feed_set_up


# ------------------------------
# SETTINGS
# ------------------------------
# Articles published within this many hours are marked as fresh
FRESH_HOURS = 3


# ------------------------------
# MESSAGE FUNCTIONS
# ------------------------------
def build_empty_message(icon_name: str, heading_text: str, message_text: str) -> None:
    """
    Show a friendly, centred message when there's nothing to show.

    Parameters:
        icon_name (str): A Material icon name, e.g. "search_off"
        heading_text (str): A short heading, e.g. "No matches"
        message_text (str): What the reader can do about it.

    Returns:
        None: The message is added to the screen.
    """
    with ui.column().classes("news-empty w-full items-center text-center gap-2 py-16 opacity-80"):
        ui.icon(icon_name, size="3rem").classes("opacity-50")
        ui.label(heading_text).classes("text-lg font-medium")
        ui.label(message_text).classes("text-sm max-w-md")


def build_loading_message() -> None:
    """
    Show a spinner while the news downloads for the first time.

    Returns:
        None: The spinner is added to the screen.
    """
    with ui.column().classes("news-empty w-full items-center gap-3 py-16"):
        ui.spinner(size="lg")
        ui.label("Fetching today's news…").classes("opacity-70")


# ------------------------------
# ARTICLE PARTS
# ------------------------------
def get_fresh_class(entry: feedparser.FeedParserDict) -> str:
    """
    Get the class name that marks an article as fresh, if it is.

    Parameters:
        entry (feedparser.FeedParserDict): A news entry.

    Returns:
        str: "is-fresh" if published within FRESH_HOURS, otherwise "".
    """
    return "is-fresh" if is_recently_published(get_entry_datetime(entry), FRESH_HOURS) else ""


def build_meta_row(entry: feedparser.FeedParserDict) -> None:
    """
    Show the small row of details for an article: source and website on the left, time on the right.

    Parameters:
        entry (feedparser.FeedParserDict): A news entry labelled with "source_name".

    Returns:
        None: The row is added to the screen.
    """
    with ui.row().classes("news-meta w-full items-baseline no-wrap gap-x-3 text-xs"):
        ui.label(entry.get("source_name", "")).classes("news-source font-medium shrink-0")
        ui.label(get_publisher_name(entry.get("link", ""))).classes("news-publisher opacity-60 truncate")
        ui.space()  # Pushes the time to the far right
        ui.label(format_time_ago(get_entry_datetime(entry))).classes("news-time opacity-60 shrink-0 tabular-nums")


def build_open_original_button(entry: feedparser.FeedParserDict) -> None:
    """
    Show a small button that opens the article's original page.

    Parameters:
        entry (feedparser.FeedParserDict): A news entry.

    Returns:
        None: The button is added to the screen.
    """
    article_link = entry.get("link", "")
    ui.button(icon="open_in_new", on_click=lambda: open_original_article(article_link)) \
        .props("flat round dense size=sm").tooltip("Open the original article")


def build_clickable_headline(entry: feedparser.FeedParserDict, search_terms: list[str],
                             open_reader: Callable[[feedparser.FeedParserDict], None], size_classes: str) -> None:
    """
    Show a headline that opens the reading panel when clicked (or when Enter is pressed on it).

    Parameters:
        entry (feedparser.FeedParserDict): A news entry.
        search_terms (list[str]): Terms to highlight.
        open_reader (Callable[[feedparser.FeedParserDict], None]): Opens the reading panel for an entry.
        size_classes (str): Text size classes, e.g. "text-lg font-semibold"

    Returns:
        None: The headline is added to the screen.
    """
    # tabindex=0 lets keyboard users reach the headline with Tab; entry=entry stores this headline's entry
    ui.html(highlight_search_terms(entry.get("title", ""), search_terms)) \
        .classes(f"news-title {size_classes} leading-snug cursor-pointer hover:underline") \
        .props('tabindex=0 role=link') \
        .on("click", lambda entry=entry: open_reader(entry)) \
        .on("keydown.enter", lambda entry=entry: open_reader(entry))


# ------------------------------
# ARTICLE LAYOUTS
# ------------------------------
def build_headline_row(entry: feedparser.FeedParserDict, search_terms: list[str],
                       open_reader: Callable[[feedparser.FeedParserDict], None]) -> None:
    """
    Show one article as a compact row: headline and a small line of details.

    Parameters:
        entry (feedparser.FeedParserDict): The news entry to show.
        search_terms (list[str]): Terms to highlight.
        open_reader (Callable[[feedparser.FeedParserDict], None]): Opens the reading panel for an entry.

    Returns:
        None: The row is added to the screen.
    """
    with ui.row().classes(f"news-row {get_fresh_class(entry)} w-full items-center no-wrap gap-2 py-3 border-b border-gray-500/20"):
        with ui.column().classes("gap-1 grow min-w-0"):
            build_clickable_headline(entry, search_terms, open_reader, "font-medium")
            build_meta_row(entry)
        build_open_original_button(entry)


def build_article_card(entry: feedparser.FeedParserDict, search_terms: list[str], show_extra_details: bool,
                       open_reader: Callable[[feedparser.FeedParserDict], None]) -> None:
    """
    Show one article as a card with its headline, summary and buttons.

    Parameters:
        entry (feedparser.FeedParserDict): The news entry to show.
        search_terms (list[str]): Terms to highlight.
        show_extra_details (bool): True to also show the exact date and link.
        open_reader (Callable[[feedparser.FeedParserDict], None]): Opens the reading panel for an entry.

    Returns:
        None: The card is added to the screen.
    """
    with ui.card().classes(f"news-card {get_fresh_class(entry)} w-full gap-2").props("flat bordered"):
        build_meta_row(entry)
        build_clickable_headline(entry, search_terms, open_reader, "text-lg font-semibold")

        summary_text = entry.get("summary", "")
        if summary_text:
            ui.html(highlight_search_terms(summary_text, search_terms)).classes("news-summary text-sm leading-relaxed opacity-90")

        # The "Detailed" view adds the exact date and the link
        if show_extra_details:
            with ui.column().classes("news-details gap-0 text-xs opacity-60"):
                ui.label(format_exact_date(get_entry_datetime(entry)))
                ui.label(entry.get("link", "")).classes("break-all")

        with ui.row().classes("news-actions items-center gap-1 -ml-2"):
            ui.button("Read full article", icon="menu_book", on_click=lambda entry=entry: open_reader(entry)) \
                .props("flat dense no-caps")
            build_open_original_button(entry)


# ------------------------------
# NEWS LIST FUNCTION
# ------------------------------
def build_news_list(visible_entries: list[feedparser.FeedParserDict], matching_entry_count: int,
                    reader_state: ReaderState,
                    open_reader: Callable[[feedparser.FeedParserDict], None]) -> None:
    """
    Show the articles in the reader's chosen view, or a message if there are none.

    Parameters:
        visible_entries (list[feedparser.FeedParserDict]): The articles to show, already sorted and limited.
        matching_entry_count (int): How many articles matched before the per-source limit.
        reader_state (ReaderState): The reader's choices.
        open_reader (Callable[[feedparser.FeedParserDict], None]): Opens the reading panel for an entry.

    Returns:
        None: The list is added to the screen.
    """
    search_terms = split_search_text(reader_state.search_text)

    # First run: no feeds have been added yet
    if not any(is_feed_set_up(feed_url) for feed_url in FEEDS.values()):
        build_empty_message("add_link", "Add your first feed",
                            "Open settings/feeds.py, replace PLACEHOLDER_URL with an RSS feed URL in quotes, "
                            "then restart the app. docs/ADDING_FEEDS.md explains where to find feeds.")
        return

    # Nothing ticked
    if not reader_state.chosen_source_names:
        build_empty_message("checklist", "Choose a source", "Tick at least one source in the sidebar to see its news.")
        return

    # Ticked, but nothing to show
    if not visible_entries:
        if search_terms:
            hint = " Try turning off “Match all terms”." if reader_state.match_all_terms else " Try another word, or tick more sources."
            build_empty_message("search_off", "No matches", f"None of your chosen sources mention “{reader_state.search_text}”.{hint}")
        else:
            build_empty_message("inbox", "Nothing here yet", "Your chosen sources have no articles right now.")
        return

    # A short line saying how many articles are shown
    count_text = f"{len(visible_entries)} article" + ("" if len(visible_entries) == 1 else "s")
    if matching_entry_count > len(visible_entries):
        count_text += f", plus {matching_entry_count - len(visible_entries)} more hidden by the per-source limit"
    ui.label(count_text).classes("news-count text-xs opacity-60")

    # The headlines view is a tight list; the other two use cards
    if reader_state.view_mode == "headlines":
        with ui.column().classes("w-full gap-0"):
            for entry in visible_entries:
                build_headline_row(entry, search_terms, open_reader)
    else:
        show_extra_details = reader_state.view_mode == "detailed"
        with ui.column().classes("w-full gap-3"):
            for entry in visible_entries:
                build_article_card(entry, search_terms, show_extra_details, open_reader)
