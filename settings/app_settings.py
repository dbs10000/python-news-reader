# ==========================================================================
# APP SETTINGS
# ------------------------------
# How the app runs and what it shows when it first opens. Change these freely.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports the os module for reading settings from the computer or hosting service
import os


# ------------------------------
# HOW THE APP RUNS
# ------------------------------
# "desktop" opens the app in its own window.
# "website" serves it as a web page, either on your computer or on a hosting service.
# A hosting service can override this without you editing the file, by setting APP_MODE=website.
APP_MODE = os.environ.get("APP_MODE", "website")

# The name shown in the window title, browser tab and header
APP_TITLE = "News"

# Desktop mode only: the window's starting size as (width, height) in pixels
WINDOW_SIZE = (1280, 860)

# Website mode only: the port the site runs on. Hosting services set their own PORT, which wins.
WEBSITE_PORT = int(os.environ.get("PORT", 8080))

# Website mode only: open your browser automatically when the site starts on your computer
OPEN_BROWSER_ON_START = APP_MODE == "website" and "PORT" not in os.environ

# ------------------------------
# LOOK
# ------------------------------
# The app's design: "ink", "frost", "signal" or "classic". See gui/themes.py.
# To try one without changing this, add ?theme=frost (for example) to the end of the web address.
THEME = "frost"

# Only used by themes that don't choose for themselves (Classic):
# None follows your computer's light/dark setting; True is always dark; False is always light
DARK_MODE = None


# ------------------------------
# NEWS
# ------------------------------
# How old the news can get (in minutes) before it is downloaded again automatically
REFRESH_MINUTES = 30


# ------------------------------
# STARTING CHOICES
# ------------------------------
# Options for the "Articles per source" dropdown, mapped to the label shown. 0 means all of them.
ENTRIES_PER_SOURCE_OPTIONS = {5: "5", 10: "10", 20: "20", 0: "All"}
DEFAULT_ENTRIES_PER_SOURCE = 5

# Options for the "Show" switch, mapped to the label shown
VIEW_MODE_OPTIONS = {
    "headlines": "Headlines",  # A compact list of headlines to skim
    "summaries": "Summaries",  # Headlines with their summaries
    "detailed": "Detailed",    # Summaries plus the exact date and link
}
DEFAULT_VIEW_MODE = "summaries"
