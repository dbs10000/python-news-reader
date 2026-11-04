# ==========================================================================
# LINKS
# ------------------------------
# Opens an article's original web page in the right place for the app mode.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports webbrowser for opening links in your normal browser
import webbrowser

# External Modules
# ------------------------------
# Imports NiceGUI's ui, for opening links in a new browser tab
from nicegui import ui

# Project Modules
# ------------------------------
# Imports the app mode setting
from settings.app_settings import APP_MODE


# ------------------------------
# LINK FUNCTION
# ------------------------------
def open_original_article(article_link: str) -> None:
    """
    Open an article's original page: in your normal browser for the desktop app,
    or in a new tab for the website.

    Parameters:
        article_link (str): The article's web address.

    Returns:
        None
    """
    if not article_link:
        return

    if APP_MODE == "desktop":
        webbrowser.open(article_link)  # The desktop app runs on your computer, so open your browser
    else:
        ui.navigate.to(article_link, new_tab=True)  # Ask the visitor's browser to open a new tab
