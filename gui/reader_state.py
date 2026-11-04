# ==========================================================================
# READER STATE
# ------------------------------
# Remembers what one reader has chosen on screen: sources, view, search and so on.
# Each open window or website visitor gets their own copy.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports dataclass, a quick way to make a class that just holds named values
from dataclasses import dataclass, field

# Project Modules
# ------------------------------
# Imports the starting choices
from settings.app_settings import DEFAULT_ENTRIES_PER_SOURCE, DEFAULT_VIEW_MODE


# ------------------------------
# READER STATE CLASS
# ------------------------------
@dataclass
class ReaderState:
    """
    The choices one reader has made on screen.

    Attributes:
        chosen_source_names (set[str]): The sources ticked in the sidebar.
        entries_per_source (int): How many articles to show from each source (0 means all).
        view_mode (str): "headlines", "summaries" or "detailed".
        search_text (str): What's typed in the search box.
        match_all_terms (bool): True to show only articles containing every search term.
        reader_article_link (str): The link of the article open in the reading panel.
    """
    # field(default_factory=set) gives each reader their own empty set, rather than one shared set
    chosen_source_names: set[str] = field(default_factory=set)
    entries_per_source: int = DEFAULT_ENTRIES_PER_SOURCE
    view_mode: str = DEFAULT_VIEW_MODE
    search_text: str = ""
    match_all_terms: bool = False
    reader_article_link: str = ""
