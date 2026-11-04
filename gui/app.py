# ==========================================================================
# APP
# ------------------------------
# Builds the page (header, sidebar, search, news list, reading panel), connects them together,
# and starts the app as a desktop window or a website.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports asyncio, used for a lock that stops two downloads of the news happening at once
import asyncio
# Imports Path, for finding the fonts folder next to this file
from pathlib import Path

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser
# Imports NiceGUI: app (the running app), run (slow jobs in the background) and ui (the screen)
from nicegui import app, run, ui

# Project Modules
# ------------------------------
# Imports the app settings
from settings.app_settings import (
    APP_MODE, APP_TITLE, WINDOW_SIZE, WEBSITE_PORT, OPEN_BROWSER_ON_START, DARK_MODE, REFRESH_MINUTES, THEME,
)
# Imports the shared store of downloaded news
from feeds.news_store import news_store
# Imports the functions that gather, de-duplicate, sort and limit articles
from selection.arrange import (
    collect_entries_from_sources, remove_duplicate_entries, sort_entries_newest_first, limit_entries_per_source,
)
# Imports the search functions
from search.search import split_search_text, filter_entries_by_search
# Imports the pieces of the screen
from gui.reader_state import ReaderState
from gui.formatting import format_time_ago
from gui.sidebar import build_display_controls, build_source_checkboxes
from gui.news_list import build_news_list, build_loading_message
from gui.reader_panel import build_reader_drawer, show_article_in_reader
from gui.themes import apply_theme


# ------------------------------
# SETTINGS
# ------------------------------
# The folder holding the bundled fonts, which the browser loads from /fonts
FONTS_FOLDER = Path(__file__).parent / "fonts"


# ------------------------------
# NEWS FUNCTIONS
# ------------------------------
# Only one download at a time, even if several windows ask at once
news_download_lock = asyncio.Lock()


async def refresh_news(force_refresh: bool = False) -> None:
    """
    Download the news again if it's out of date (or always, if forced), without freezing the screen.

    Parameters:
        force_refresh (bool): True to download even if the news is still fresh.

    Returns:
        None: The shared news store is updated.
    """
    async with news_download_lock:  # Wait here if another download is already running
        if force_refresh or news_store.is_out_of_date(REFRESH_MINUTES):
            await run.io_bound(news_store.refresh)  # Download in the background


def find_visible_entries(reader_state: ReaderState) -> tuple[list[feedparser.FeedParserDict], int]:
    """
    Work out which articles to show, based on the reader's choices.

    Parameters:
        reader_state (ReaderState): The reader's choices.

    Returns:
        tuple[list[feedparser.FeedParserDict], int]: In the form (visible_entries, matching_entry_count).
            matching_entry_count is how many matched before the per-source limit was applied.
    """
    news_entries = collect_entries_from_sources(news_store.all_feeds, reader_state.chosen_source_names)
    news_entries = remove_duplicate_entries(news_entries)  # Drop repeated stories
    news_entries = filter_entries_by_search(
        news_entries, split_search_text(reader_state.search_text), reader_state.match_all_terms,
    )
    news_entries = sort_entries_newest_first(news_entries)  # Newest first, so the limit keeps the latest

    matching_entry_count = len(news_entries)  # Count before limiting, so the reader knows what's hidden
    visible_entries = limit_entries_per_source(news_entries, reader_state.entries_per_source)

    return visible_entries, matching_entry_count


def choose_sources_with_entries(reader_state: ReaderState) -> None:
    """
    Tick every source that has articles, for a reader who hasn't chosen any yet.

    Parameters:
        reader_state (ReaderState): The reader's choices, updated in place.

    Returns:
        None
    """
    reader_state.chosen_source_names = {name for name, feed in news_store.all_feeds.items() if feed.entries}


# ------------------------------
# PAGE
# ------------------------------
@ui.page("/")  # This function builds the page whenever a window opens or someone visits the site
def news_page(theme: str | None = None) -> None:
    """
    Build the news page for one reader.

    Parameters:
        theme (str | None): A theme to preview, taken from the web address, e.g. /?theme=frost.
            None uses THEME from settings.

    Returns:
        None: The page is created on screen.
    """
    reader_state = ReaderState()  # This reader's own choices
    has_loaded_once = {"value": False}  # A dictionary so the functions below can change it

    apply_theme(theme or THEME, DARK_MODE)  # Fonts, colours and styles

    # ------------------------------
    # Parts of the page that get redrawn
    # ------------------------------
    # @ui.refreshable lets a part of the page be rebuilt by calling its .refresh()

    @ui.refreshable
    def show_updated_time() -> None:
        """Show when the news was last downloaded, e.g. "Updated 4 min ago"."""
        if news_store.last_updated is not None:
            ui.label(f"Updated {format_time_ago(news_store.last_updated)}").classes("news-updated text-xs opacity-80")

    @ui.refreshable
    def show_sources() -> None:
        """Show the source checkboxes."""
        if has_loaded_once["value"]:
            build_source_checkboxes(news_store.all_feeds, news_store.failed_source_names, reader_state,
                                    update_news, update_sources_and_news)

    @ui.refreshable
    def show_news() -> None:
        """Show the news list, or a spinner before the first download finishes."""
        if not has_loaded_once["value"]:
            build_loading_message()
            return
        visible_entries, matching_entry_count = find_visible_entries(reader_state)
        build_news_list(visible_entries, matching_entry_count, reader_state, open_reader)

    def update_news() -> None:
        """Redraw just the news list."""
        show_news.refresh()

    def update_sources_and_news() -> None:
        """Redraw the source checkboxes and the news list."""
        show_sources.refresh()
        show_news.refresh()

    def update_everything() -> None:
        """Redraw every part that depends on the downloaded news."""
        show_updated_time.refresh()
        update_sources_and_news()

    # ------------------------------
    # Actions
    # ------------------------------
    async def open_reader(entry: feedparser.FeedParserDict) -> None:
        """Open the reading panel for an article."""
        await show_article_in_reader(reader_drawer, reader_content, entry, reader_state)

    async def load_news_for_first_time() -> None:
        """Wait for the news, tick the sources that have articles, then draw everything."""
        await refresh_news()
        choose_sources_with_entries(reader_state)
        has_loaded_once["value"] = True
        update_everything()

    async def refresh_when_clicked() -> None:
        """Download the news again when the refresh button is clicked."""
        refresh_button.props("loading")  # Show a spinner on the button
        await refresh_news(force_refresh=True)
        refresh_button.props(remove="loading")
        update_everything()
        ui.notify("News updated", type="positive", position="bottom")

    async def refresh_if_out_of_date() -> None:
        """Every so often, download the news again if it's old, so an open window stays current."""
        if news_store.is_out_of_date(REFRESH_MINUTES):
            await refresh_news()
            update_everything()

    def change_search(event) -> None:
        """Remember the new search text and redraw the news."""
        reader_state.search_text = event.value or ""  # The clear button sets None, so use "" instead
        update_news()

    def change_match_all(event) -> None:
        """Remember the "Match all terms" switch and redraw the news."""
        reader_state.match_all_terms = event.value
        update_news()

    # ------------------------------
    # Layout
    # ------------------------------
    # Header across the top
    with ui.header(elevated=False).classes("items-center gap-2 px-3 py-2"):
        ui.button(icon="menu", on_click=lambda: sidebar.toggle()).props("flat round color=white").tooltip("Show or hide controls")
        ui.label(APP_TITLE).classes("news-brand text-lg font-semibold")
        ui.space()
        show_updated_time()
        refresh_button = ui.button(icon="refresh", on_click=refresh_when_clicked) \
            .props("flat round color=white").tooltip("Get the latest news")

    # Sidebar on the left (shown on wide screens, hidden behind the menu button on narrow ones)
    with ui.left_drawer(bordered=True).props("width=304").classes("news-sidebar px-4 pb-6") as sidebar:
        build_display_controls(reader_state, update_news)
        show_sources()

    # Reading panel on the right (hidden until an article is opened)
    reader_drawer, reader_content = build_reader_drawer()

    # Main area: search bar and news, kept to a comfortable reading width
    with ui.column().classes("news-main w-full max-w-3xl mx-auto gap-3 px-2 sm:px-4 py-4"):
        with ui.row().classes("w-full items-center gap-3"):
            # debounce=300 waits until typing pauses for 0.3 seconds, so it doesn't redraw on every key
            with ui.input(placeholder="Search, e.g. nvidia, oil", on_change=change_search) \
                    .props("outlined dense clearable debounce=300").classes("news-search grow min-w-[220px]") as search_box:
                with search_box.add_slot("prepend"):
                    ui.icon("search")
            ui.switch("Match all terms", on_change=change_match_all).props("dense") \
                .tooltip("On: show articles mentioning every term. Off: any of them.")
        show_news()

    # Timers: load the news straight after the page appears, then keep things up to date
    ui.timer(0.1, load_news_for_first_time, once=True)
    ui.timer(60, show_updated_time.refresh)  # Keep "Updated x min ago" accurate
    ui.timer(5 * 60, refresh_if_out_of_date)  # Check every 5 minutes whether the news is old


# ------------------------------
# START FUNCTION
# ------------------------------
def start_app() -> None:
    """
    Start the app as a desktop window or a website, depending on APP_MODE in settings.

    Returns:
        None: Runs until the window is closed or the server is stopped.
    """
    app.on_startup(refresh_news)  # Start downloading the news as soon as the app starts
    app.add_static_files("/fonts", FONTS_FOLDER)  # Let the browser load the bundled fonts

    if APP_MODE == "desktop":
        # native=True opens a real window instead of a browser tab
        ui.run(title=APP_TITLE, native=True, window_size=WINDOW_SIZE, dark=DARK_MODE, reload=False, favicon="📰")
    else:
        # host="0.0.0.0" lets other devices (or a hosting service) reach the site
        ui.run(title=APP_TITLE, host="0.0.0.0", port=WEBSITE_PORT, show=OPEN_BROWSER_ON_START,
               dark=DARK_MODE, reload=False, favicon="📰")
