# ==========================================================================
# SIDEBAR
# ------------------------------
# The controls on the left: what to show, how many per source, and which sources.
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
# Imports the grouped sources, which become the sidebar headings
from settings.feeds import FEED_GROUPS
# Imports the dropdown and switch options
from settings.app_settings import ENTRIES_PER_SOURCE_OPTIONS, VIEW_MODE_OPTIONS
# Imports the reader's choices
from gui.reader_state import ReaderState
# Imports the check for whether a source has a real feed URL yet
from feeds.fetch import is_feed_set_up


# ------------------------------
# SMALL PIECES
# ------------------------------
def build_section_label(label_text: str) -> None:
    """
    Show a small grey heading above a group of controls.

    Parameters:
        label_text (str): The heading, e.g. "Show"

    Returns:
        None: The label is added to the screen.
    """
    ui.label(label_text).classes("sidebar-label text-xs font-medium opacity-60 mt-5 mb-1.5")


# ------------------------------
# DISPLAY CONTROLS
# ------------------------------
def build_display_controls(reader_state: ReaderState, update_news: Callable[[], None]) -> None:
    """
    Show the "Show" switch and the "Articles per source" dropdown.

    Parameters:
        reader_state (ReaderState): The reader's choices, updated when a control changes.
        update_news (Callable[[], None]): Redraws the news; called after every change.

    Returns:
        None: The controls are added to the screen.
    """

    def change_view_mode(event) -> None:
        """Remember the new view and redraw the news."""
        reader_state.view_mode = event.value
        update_news()

    def change_entries_per_source(event) -> None:
        """Remember the new limit and redraw the news."""
        reader_state.entries_per_source = event.value
        update_news()

    build_section_label("Show")
    ui.toggle(VIEW_MODE_OPTIONS, value=reader_state.view_mode, on_change=change_view_mode) \
        .props("spread no-caps unelevated toggle-color=selected toggle-text-color=onselected").classes("w-full")

    build_section_label("Articles per source")
    ui.select(ENTRIES_PER_SOURCE_OPTIONS, value=reader_state.entries_per_source, on_change=change_entries_per_source) \
        .props("outlined dense options-dense").classes("w-full")


# ------------------------------
# SOURCE CHECKBOXES
# ------------------------------
def build_source_checkboxes(all_feeds: dict[str, feedparser.FeedParserDict],
                            failed_source_names: list[str],
                            reader_state: ReaderState,
                            update_news: Callable[[], None],
                            update_sources_and_news: Callable[[], None]) -> None:
    """
    Show a checkbox for every source, under its group heading, with its number of articles.

    Parameters:
        all_feeds (dict[str, feedparser.FeedParserDict]): Source names mapped to their parsed feeds.
        failed_source_names (list[str]): Sources that couldn't be read, shown with a warning.
        reader_state (ReaderState): The reader's choices, updated when a box is ticked.
        update_news (Callable[[], None]): Redraws the news after one box changes.
        update_sources_and_news (Callable[[], None]): Redraws the boxes and news after "All" or "None".

    Returns:
        None: The checkboxes are added to the screen.
    """

    def choose_all_sources() -> None:
        """Tick every source that has articles."""
        reader_state.chosen_source_names = {name for name, feed in all_feeds.items() if feed.entries}
        update_sources_and_news()

    def choose_no_sources() -> None:
        """Untick every source."""
        reader_state.chosen_source_names = set()
        update_sources_and_news()

    def change_source(source_name: str, is_ticked: bool) -> None:
        """Add or remove one source from the reader's choices, then redraw the news."""
        if is_ticked:
            reader_state.chosen_source_names.add(source_name)
        else:
            reader_state.chosen_source_names.discard(source_name)  # discard doesn't fail if it's missing
        update_news()

    # Heading with "All" and "None" shortcuts
    with ui.row().classes("w-full items-center justify-between mt-5"):
        ui.label("Sources").classes("sidebar-label text-xs font-medium opacity-60")
        with ui.row().classes("gap-0"):
            ui.button("All", on_click=choose_all_sources).props("flat dense no-caps size=sm")
            ui.button("None", on_click=choose_no_sources).props("flat dense no-caps size=sm")

    # One heading per group, with its sources underneath
    for group_name, group_feeds in FEED_GROUPS.items():
        ui.label(group_name).classes("sidebar-group text-sm font-medium mt-3 mb-1")

        for source_name, feed_url in group_feeds.items():
            # A source that still has the placeholder URL is shown as waiting to be set up
            if not is_feed_set_up(feed_url):
                with ui.row().classes("w-full items-center no-wrap gap-2 pl-0.5 opacity-50") as not_set_up_row:
                    ui.icon("add_link", size="xs")
                    ui.label(source_name).classes("text-sm grow")
                    ui.label("not set up").classes("text-xs")
                not_set_up_row.tooltip("Paste a feed URL for this source in settings/feeds.py, then restart the app.")
                continue

            # A source that failed to download gets a warning instead of a checkbox
            if source_name in failed_source_names:
                with ui.row().classes("w-full items-center no-wrap gap-2 pl-0.5 opacity-60") as failed_row:
                    ui.icon("error_outline", color="red-4", size="xs")  # A softer red that shows on light and dark themes
                    ui.label(source_name).classes("text-sm grow")
                    ui.label("failed").classes("text-xs")
                failed_row.tooltip("This feed couldn't be downloaded. Try refreshing, or check its URL in settings/feeds.py.")
                continue

            entry_count = len(all_feeds[source_name].entries) if source_name in all_feeds else 0

            # Empty sources are faded so the ones with news stand out
            row_fade = "opacity-40" if entry_count == 0 else ""
            with ui.row().classes(f"source-row w-full items-center justify-between no-wrap {row_fade}"):
                # name=source_name stores this loop's name, so each checkbox changes its own source
                source_checkbox = ui.checkbox(
                    source_name,
                    value=source_name in reader_state.chosen_source_names,
                    on_change=lambda event, name=source_name: change_source(name, event.value),
                ).props("dense").classes("text-sm")
                ui.label(str(entry_count)).classes("text-xs opacity-60 tabular-nums")

                # A source with nothing in it today can't be ticked, which shows at a glance it's empty
                if entry_count == 0:
                    source_checkbox.disable()
                    source_checkbox.tooltip("No articles today")
