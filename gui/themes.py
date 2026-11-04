# ==========================================================================
# THEMES
# ------------------------------
# The look of the app. Each theme is a set of colours, fonts and styles (CSS).
# Pick one with THEME in settings/app_settings.py, or preview any theme by adding
# ?theme=ink (or frost, signal, classic) to the end of the web address.
# ==========================================================================

# ------------------------------
# MODULES
# ------------------------------

# Built-in Modules
# ------------------------------
# Imports dataclass, a quick way to make a class that just holds named values
from dataclasses import dataclass

# External Modules
# ------------------------------
# Imports NiceGUI's ui, for adding styles and colours to the page
from nicegui import ui


# ------------------------------
# THEME CLASS
# ------------------------------
@dataclass(frozen=True)  # frozen=True means a theme can't be changed by accident once made
class Theme:
    """
    One look for the app.

    Attributes:
        label (str): The theme's display name, e.g. "Ink"
        primary_colour (str): The main colour for buttons, ticks and switches, as a hex code.
        dark_mode (bool | None): True for dark, False for light, None to follow the computer.
        css (str): The styles that make this theme look the way it does.
        selected_colour (str): The background of the chosen option in the Show switch.
        on_selected_colour (str): The text colour on top of selected_colour.
    """
    label: str
    primary_colour: str
    dark_mode: bool | None
    css: str
    selected_colour: str
    on_selected_colour: str


# ------------------------------
# FONTS
# ------------------------------
# The fonts are stored in gui/fonts, so the app works offline. Each font has two files:
# one for everyday letters (latin) and one for accented letters (latin-ext).
LATIN_RANGE = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
               "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
LATIN_EXT_RANGE = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,"
                   "U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")

# Font names used in CSS, mapped to the start of their file names in gui/fonts
FONT_FILES = {
    "Newsreader": "newsreader",
    "Geist": "geist",
    "Sora": "sora",
    "Schibsted Grotesk": "schibsted-grotesk",
}


def build_font_css() -> str:
    """
    Write the CSS that tells the browser where each bundled font file is.

    Returns:
        str: One @font-face rule per font file.
    """
    font_rules = []  # Stores one rule per font file

    for font_name, file_start in FONT_FILES.items():
        # Each font has a latin file and a latin-ext file, each covering its own range of characters
        for file_part, character_range in (("latin", LATIN_RANGE), ("latin-ext", LATIN_EXT_RANGE)):
            font_rules.append(
                f"@font-face {{ font-family: '{font_name}'; font-style: normal; font-display: swap; "
                f"font-weight: 100 900; src: url('/fonts/{file_start}-{file_part}-wght-normal.woff2') format('woff2'); "
                f"unicode-range: {character_range}; }}"
            )

    return "\n".join(font_rules)


# ------------------------------
# SHARED STYLES
# ------------------------------
# Styles every theme uses. Theme styles come afterwards, so they can override these.
SHARED_CSS = """
mark { background: #fde047; color: #1f2937; border-radius: 3px; padding: 0 2px; }
/* On phones, let the reading panel fill the screen instead of being wider than it */
@media (max-width: 680px) { .q-drawer--right { width: 100vw !important; } }
/* Keep article text at a comfortable line length */
.reader-text, .reader-title { max-width: 64ch; }
/* Show keyboard users where they are */
.q-btn:focus-visible, .news-title:focus-visible { outline: 2px solid var(--q-primary); outline-offset: 2px; }
/* Fresh articles: the time is shown in the main colour */
.is-fresh .news-time { color: var(--q-primary); opacity: 1 !important; font-weight: 600; }
"""


# ------------------------------
# CLASSIC THEME
# ------------------------------
# The original look: standard Material Design blue.
CLASSIC = Theme(label="Classic", primary_colour="#1976d2", dark_mode=None, css="",
                selected_colour="#1976d2", on_selected_colour="#FFFFFF")


# ------------------------------
# INK THEME
# ------------------------------
# Black and white, like a quiet printed page: large serif headlines and lots of space.
INK = Theme(label="Ink", primary_colour="#000000", dark_mode=False, css="""
body.theme-ink { background: #FFFFFF; color: #000000; font-family: 'Geist', system-ui, sans-serif; }

/* Header: white with a thin rule underneath */
.theme-ink .q-header { background: #FFFFFF !important; color: #000000; box-shadow: none !important;
    border-bottom: 1px solid #E4E4E4; }
.theme-ink .q-header .q-btn, .theme-ink .q-header .q-icon { color: #000000 !important; }
.theme-ink .news-brand { font-family: 'Newsreader', serif; font-size: 26px; font-weight: 500; letter-spacing: -0.01em; }
.theme-ink .news-updated { color: #6B6B6B; opacity: 1; }

/* Sidebar */
.theme-ink .q-drawer { background: #FFFFFF; }
.theme-ink .q-drawer--left.q-drawer--bordered { border-right: 1px solid #E4E4E4; }
.theme-ink .sidebar-label { color: #6B6B6B; opacity: 1; }
.theme-ink .sidebar-group { font-family: 'Newsreader', serif; font-size: 17px; font-weight: 500; }
.theme-ink .q-btn-toggle { border: 1px solid #000000; border-radius: 0; }
.theme-ink .q-btn-toggle .q-btn { border-radius: 0; }
.theme-ink .q-field--outlined .q-field__control { border-radius: 0; }
.theme-ink .q-field--outlined .q-field__control:before { border-color: #000000; }

/* Articles: no boxes, just space and a thin rule between them */
.theme-ink .news-card { background: transparent; border: 0; border-bottom: 1px solid #E4E4E4;
    border-radius: 0; box-shadow: none; padding: 28px 0 22px; }
.theme-ink .news-row { border-bottom: 1px solid #E4E4E4; padding: 16px 0; }
.theme-ink .news-title { font-family: 'Newsreader', serif; font-weight: 500; font-size: 30px;
    line-height: 1.12; letter-spacing: -0.018em; }
.theme-ink .news-row .news-title { font-size: 21px; line-height: 1.25; letter-spacing: -0.01em; }
.theme-ink .news-summary { font-family: 'Newsreader', serif; font-size: 18px; line-height: 1.55;
    color: #2B2B2B; opacity: 1; max-width: 62ch; }
.theme-ink .news-meta { font-size: 12.5px; }
.theme-ink .news-source { color: #000000; }
.theme-ink .news-publisher, .theme-ink .news-time, .theme-ink .news-details, .theme-ink .news-count { color: #6B6B6B; opacity: 1; }
.theme-ink .is-fresh .news-time { color: #000000; }
.theme-ink .is-fresh .news-time::before { content: ""; display: inline-block; width: 6px; height: 6px;
    background: #000000; border-radius: 50%; margin-right: 6px; vertical-align: 2px; }
.theme-ink mark { background: #000000; color: #FFFFFF; border-radius: 0; padding: 0 3px; }

/* Reading panel: a clean page */
.theme-ink .q-drawer--right { background: #FFFFFF; box-shadow: -1px 0 0 #E4E4E4 !important; }
.theme-ink .reader-title { font-family: 'Newsreader', serif; font-size: 38px; font-weight: 500;
    line-height: 1.1; letter-spacing: -0.02em; }
.theme-ink .reader-text { font-family: 'Newsreader', serif; font-size: 20px; line-height: 1.65; color: #111111; }
.theme-ink .q-btn--outline { border-radius: 0; }
.theme-ink .reader-notice { background: #F4F4F4; border-radius: 0; }

/* Smaller type on phones, so a headline fits in a few lines */
@media (max-width: 600px) {
    .theme-ink .news-title { font-size: 24px; }
    .theme-ink .news-summary { font-size: 16.5px; }
    .theme-ink .reader-title { font-size: 30px; }
    .theme-ink .reader-text { font-size: 18px; }
}
""", selected_colour="#000000", on_selected_colour="#FFFFFF")


# ------------------------------
# FROST THEME
# ------------------------------
# Glassmorphism: frosted, see-through panels floating over a soft dawn of teal and amber.
FROST_GLASS = "background: rgba(255,255,255,0.08); backdrop-filter: blur(22px) saturate(150%); " \
              "-webkit-backdrop-filter: blur(22px) saturate(150%); border: 1px solid rgba(255,255,255,0.16);"

FROST = Theme(label="Frost", primary_colour="#F2B880", dark_mode=True, css=f"""
body.theme-frost {{ font-family: 'Sora', system-ui, sans-serif; color: #F4F8FA;
    background-color: #0B1F2E !important;
    background-image:
        radial-gradient(60vw 55vw at 8% -5%, rgba(30,122,140,0.85), transparent 62%),
        radial-gradient(45vw 45vw at 100% 8%, rgba(242,184,128,0.55), transparent 60%),
        radial-gradient(70vw 55vw at 65% 115%, rgba(62,92,154,0.75), transparent 60%);
    background-attachment: fixed; }}

/* Header: a thin sheet of glass */
.theme-frost .q-header {{ background: rgba(11,31,46,0.30) !important; backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px); box-shadow: none !important; border-bottom: 1px solid rgba(255,255,255,0.12); }}
.theme-frost .news-brand {{ font-weight: 600; letter-spacing: -0.02em; }}

/* Sidebar: a floating pane of glass with rounded corners */
.theme-frost .q-drawer--left {{ background: transparent !important; border: 0 !important; }}
.theme-frost .q-drawer--left .q-drawer__content {{ {FROST_GLASS} border-radius: 24px; margin: 14px;
    height: calc(100% - 28px); padding-top: 4px; }}
.theme-frost .sidebar-label {{ color: rgba(244,248,250,0.62); opacity: 1; }}
.theme-frost .q-btn-toggle {{ background: rgba(255,255,255,0.07); border-radius: 999px; padding: 3px; }}
.theme-frost .q-btn-toggle .q-btn {{ border-radius: 999px; }}
.theme-frost .q-field--outlined .q-field__control {{ background: rgba(255,255,255,0.07); border-radius: 14px; }}
.theme-frost .news-search .q-field__control {{ border-radius: 999px; }}
.theme-frost .q-field--outlined .q-field__control:before {{ border-color: rgba(255,255,255,0.22); }}
.theme-frost .q-menu {{ background: rgba(16,44,62,0.82); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.14); border-radius: 14px; }}

/* Articles: glass cards */
.theme-frost .news-card {{ {FROST_GLASS} border-radius: 20px; padding: 20px 22px; box-shadow: 0 8px 32px rgba(3,14,22,0.25); }}
.theme-frost .news-row {{ border-bottom: 1px solid rgba(255,255,255,0.12); padding: 14px 4px; }}
.theme-frost .news-title {{ font-size: 19px; font-weight: 600; line-height: 1.32; letter-spacing: -0.012em; }}
.theme-frost .news-row .news-title {{ font-size: 16px; }}
.theme-frost .news-summary {{ font-size: 14.5px; line-height: 1.65; color: rgba(244,248,250,0.82); opacity: 1; }}
.theme-frost .news-publisher, .theme-frost .news-time, .theme-frost .news-details, .theme-frost .news-count {{ color: rgba(244,248,250,0.62); opacity: 1; }}
.theme-frost .is-fresh .news-time {{ color: #F2B880; }}
.theme-frost .is-fresh .news-time::before {{ content: ""; display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #F2B880; box-shadow: 0 0 10px #F2B880; margin-right: 7px; vertical-align: 1px; }}
.theme-frost mark {{ background: #F2B880; color: #0B1F2E; border-radius: 6px; padding: 0 4px; }}

/* Reading panel: a thicker sheet of glass */
.theme-frost .q-drawer--right {{ background: rgba(11,31,46,0.55) !important; backdrop-filter: blur(30px) saturate(140%);
    -webkit-backdrop-filter: blur(30px) saturate(140%); border-left: 1px solid rgba(255,255,255,0.14); }}
.theme-frost .reader-title {{ font-size: 30px; font-weight: 600; line-height: 1.2; letter-spacing: -0.02em; }}
.theme-frost .reader-text {{ font-size: 17px; line-height: 1.8; color: rgba(244,248,250,0.92); }}
.theme-frost .q-btn--outline {{ border-radius: 999px; }}
.theme-frost .reader-notice {{ background: rgba(242,184,128,0.14); border-radius: 14px; }}
""", selected_colour="#F4F8FA", on_selected_colour="#0B1F2E")


# ------------------------------
# SIGNAL THEME
# ------------------------------
# A calm dark desk for reading at night. Articles from the last few hours glow amber.
SIGNAL = Theme(label="Signal", primary_colour="#F2A33A", dark_mode=True, css="""
body.theme-signal { font-family: 'Schibsted Grotesk', system-ui, sans-serif; color: #E8EAED; background: #15181C !important; }

/* Header and sidebar share the page colour, separated by thin lines */
.theme-signal .q-header { background: #15181C !important; color: #E8EAED; box-shadow: none !important; border-bottom: 1px solid #2A2F36; }
.theme-signal .news-brand { font-weight: 700; letter-spacing: -0.025em; font-size: 20px; }
.theme-signal .q-drawer { background: #15181C !important; }
.theme-signal .q-drawer--left.q-drawer--bordered { border-right: 1px solid #2A2F36; }
.theme-signal .sidebar-label { color: #8B929B; opacity: 1; }
.theme-signal .q-btn-toggle { background: #1E2227; border: 1px solid #2A2F36; border-radius: 10px; }
.theme-signal .q-btn-toggle .q-btn { border-radius: 9px; }
.theme-signal .q-field--outlined .q-field__control { background: #1E2227; border-radius: 10px; }
.theme-signal .q-field--outlined .q-field__control:before { border-color: #2A2F36; }
.theme-signal .q-menu { background: #1E2227; border: 1px solid #2A2F36; }

/* Articles: dark panels; fresh ones carry an amber bar down their left edge */
.theme-signal .news-card { background: #1E2227; border: 1px solid #2A2F36; border-radius: 10px; padding: 18px 20px;
    box-shadow: none; position: relative; overflow: hidden; }
.theme-signal .news-row { border-bottom: 1px solid #2A2F36; padding: 13px 0 13px 14px; position: relative; }
.theme-signal .is-fresh::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: #F2A33A; }
.theme-signal .news-row.is-fresh::before { top: 12px; bottom: 12px; border-radius: 2px; }
.theme-signal .news-title { font-size: 18.5px; font-weight: 650; line-height: 1.3; letter-spacing: -0.012em; color: #F5F6F7; }
.theme-signal .news-row .news-title { font-size: 16px; font-weight: 600; }
.theme-signal .news-summary { font-size: 14.5px; line-height: 1.6; color: #B9BEC5; opacity: 1; }
.theme-signal .news-source { color: #E8EAED; }
.theme-signal .news-publisher, .theme-signal .news-time, .theme-signal .news-details, .theme-signal .news-count { color: #8B929B; opacity: 1; }
.theme-signal .is-fresh .news-time { color: #F2A33A; }
.theme-signal mark { background: rgba(242,163,58,0.22); color: #FFD9A3; border-radius: 2px; padding: 0 2px;
    box-shadow: inset 0 -2px 0 #F2A33A; }

/* Reading panel */
.theme-signal .q-drawer--right { background: #1A1D21 !important; border-left: 1px solid #2A2F36; }
.theme-signal .reader-title { font-size: 30px; font-weight: 700; line-height: 1.18; letter-spacing: -0.022em; }
.theme-signal .reader-text { font-size: 18px; line-height: 1.7; color: #D9DCE0; }
.theme-signal .q-btn--outline { border-radius: 8px; }
.theme-signal .reader-notice { background: rgba(242,163,58,0.12); border-radius: 8px; }
""", selected_colour="#F2A33A", on_selected_colour="#15181C")


# ------------------------------
# ALL THEMES DICT
# ------------------------------
# Theme names (as used in settings and ?theme=) mapped to their Theme
THEMES = {"classic": CLASSIC, "ink": INK, "frost": FROST, "signal": SIGNAL}


# ------------------------------
# APPLY FUNCTION
# ------------------------------
def apply_theme(theme_name: str, fallback_dark_mode: bool | None) -> None:
    """
    Add a theme's fonts, colours and styles to the current page.

    Parameters:
        theme_name (str): A name from THEMES, e.g. "ink". Unknown names use "classic".
        fallback_dark_mode (bool | None): The dark mode setting to use if the theme doesn't choose one.

    Returns:
        None: The page is styled.
    """
    chosen_theme = THEMES.get(theme_name, CLASSIC)  # Fall back to classic for a misspelt name

    ui.add_css(build_font_css())  # Tell the browser where the bundled fonts are
    ui.add_css(SHARED_CSS)  # Styles every theme uses
    ui.add_css(chosen_theme.css)  # This theme's own styles
    # Buttons, ticks and switches use "primary"; the Show switch uses "selected" and "onselected"
    ui.colors(primary=chosen_theme.primary_colour,
              selected=chosen_theme.selected_colour, onselected=chosen_theme.on_selected_colour)

    # Use the theme's light/dark choice, or the setting if the theme leaves it open
    ui.dark_mode(chosen_theme.dark_mode if chosen_theme.dark_mode is not None else fallback_dark_mode)

    # Label the page with the theme name, so the styles above (e.g. .theme-ink) switch on
    ui.query("body").classes(f"theme-{theme_name if theme_name in THEMES else 'classic'}")
