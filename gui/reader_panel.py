# ==========================================================================
# READER PANEL
# ------------------------------
# The panel that slides in from the right to show an article's full text,
# while the list stays where it was underneath.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# External Modules
# ------------------------------
# Imports the feedparser module, used here for its type
import feedparser
# Imports NiceGUI's run (for slow jobs that mustn't freeze the screen) and ui (for the screen)
from nicegui import run, ui

# Project Modules
# ------------------------------
# Imports the reader's choices
from gui.reader_state import ReaderState
# Imports the row of details (source, website, time) used above each headline
from gui.news_list import build_meta_row
# Imports the function that opens an article's original page
from gui.links import open_original_article
# Imports the function that downloads an article's full text
from feeds.full_text import fetch_full_article_text


# ------------------------------
# PANEL FUNCTIONS
# ------------------------------
def build_reader_drawer() -> tuple[ui.right_drawer, ui.column]:
    """
    Create the hidden reading panel on the right of the page.

    Returns:
        tuple[ui.right_drawer, ui.column]: In the form (reader_drawer, reader_content).
            The drawer is the sliding panel; the column is where the article goes.
    """
    # "overlay" slides it over the list instead of squashing it; width is in pixels
    reader_drawer = ui.right_drawer(value=False, fixed=True, elevated=True).props("overlay width=640")

    with reader_drawer:
        reader_content = ui.column().classes("w-full gap-4 p-4")

    return reader_drawer, reader_content


async def show_article_in_reader(reader_drawer: ui.right_drawer, reader_content: ui.column,
                                 entry: feedparser.FeedParserDict, reader_state: ReaderState) -> None:
    """
    Open the reading panel for an article and fill it with the article's full text.

    Parameters:
        reader_drawer (ui.right_drawer): The sliding panel.
        reader_content (ui.column): The space inside the panel for the article.
        entry (feedparser.FeedParserDict): The article to show.
        reader_state (ReaderState): The reader's choices; remembers which article is open.

    Returns:
        None: The panel is opened and filled in.
    """
    article_link = entry.get("link", "")
    reader_state.reader_article_link = article_link  # Remember which article is meant to be showing

    reader_content.clear()  # Remove the previous article

    # Show the headline and buttons straight away, with a spinner where the text will go
    with reader_content:
        with ui.row().classes("w-full items-center no-wrap gap-2"):
            with ui.element("div").classes("grow min-w-0"):
                build_meta_row(entry)
            ui.button(icon="close", on_click=reader_drawer.hide).props("flat round dense").tooltip("Close")

        ui.label(entry.get("title", "")).classes("reader-title text-2xl font-semibold leading-snug")

        ui.button("Open original", icon="open_in_new", on_click=lambda: open_original_article(article_link)) \
            .props("outline dense no-caps")
        ui.separator()

        loading_row = ui.row().classes("items-center gap-3 opacity-70")
        with loading_row:
            ui.spinner()
            ui.label("Fetching the full article…")

        article_text_area = ui.column().classes("w-full gap-4")

    reader_drawer.show()

    # Download the article in the background so the screen doesn't freeze while waiting
    full_article_text = await run.io_bound(fetch_full_article_text, article_link)

    # If the reader opened a different article while this one downloaded, don't show this one
    if reader_state.reader_article_link != article_link:
        return

    loading_row.delete()  # Remove the spinner

    with article_text_area:
        if full_article_text:
            # Show each paragraph separately, at a comfortable size for reading
            for paragraph in full_article_text.split("\n"):
                if paragraph.strip():
                    ui.label(paragraph).classes("reader-text text-[17px] leading-relaxed")
        else:
            # Explain why there's no full text, then show the snippet so there's still something to read
            with ui.row().classes("reader-notice items-start gap-2 no-wrap p-3 rounded bg-amber-500/10"):
                ui.icon("lock", color="warning")
                ui.label("This site didn't share its full text. It may be paywalled or block readers like this one. "
                         "Use “Open original” to read it on the site.").classes("text-sm")
            if entry.get("summary"):
                ui.label(entry["summary"]).classes("reader-text text-[17px] leading-relaxed opacity-80")
