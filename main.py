# ==========================================================================
# PYTHON NEWS READER
# ------------------------------
# A calm, one-screen news reader. Add your own feeds in settings/feeds.py,
# and choose website or desktop window, and a design, in settings/app_settings.py.
# This file just starts the app. Run it with:  uv run main.py   (or: python main.py)
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Project Modules
# ------------------------------
# Imports the function that builds and starts the app
from gui.app import start_app


# ------------------------------
# RUN APP
# ------------------------------
# NiceGUI's desktop window runs this file a second time behind the scenes under the name
# "__mp_main__", so both names are allowed here.
if __name__ in {"__main__", "__mp_main__"}:
    start_app()
