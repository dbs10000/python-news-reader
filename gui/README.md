# gui

Everything on screen, built with **NiceGUI**. NiceGUI turns Python into a web page; in desktop mode it shows that page in its own window instead of a browser.

| File | What it does |
|---|---|
| `app.py` | Builds the page (header, sidebar, search, list, reading panel), connects them together, and starts the app. **Start here.** |
| `reader_state.py` | `ReaderState`: remembers one reader's choices (ticked sources, view, search…). Each window or visitor gets their own. |
| `sidebar.py` | The Show switch, the Articles per source dropdown, and the source checkboxes. |
| `news_list.py` | The articles (as headline rows or cards), plus friendly messages when there's nothing to show. |
| `reader_panel.py` | The panel that slides in from the right with the full article. |
| `formatting.py` | Friendly text: `"3 h ago"`, `"reuters.com"`, and search highlighting. |
| `links.py` | Opens the original article: in your browser for the desktop app, or a new tab for the website. |
| `themes.py` | The designs (Ink, Frost, Signal, Classic): each one's colours, fonts and styles. |
| `fonts/` | The font files, stored here so every theme works offline. Their licences are alongside. |

## Themes

Choose one with `THEME` in `settings/app_settings.py`, or preview any of them by adding `?theme=frost` (or `ink`, `signal`, `classic`) to the end of the web address.

Parts of the page carry class names starting `news-`, `sidebar-` or `reader-` (for example `news-title`, `news-card`, `reader-text`). These are hooks: each theme's CSS uses them to style that part, e.g. `.theme-ink .news-title { font-family: 'Newsreader'; }`. Articles from the last 3 hours also get the class `is-fresh` (set by `FRESH_HOURS` in `news_list.py`), which each theme marks in its own way.

To make your own theme, copy one in `themes.py`, rename it (e.g. `MINE`, using `.theme-mine` in its CSS), add it to the `THEMES` dictionary, and set `THEME = "mine"`.

## How the page updates

NiceGUI doesn't run top to bottom like the old terminal version. It builds the page once, then **waits for events** (a click, a tick, typing) and runs the function attached to each one.

```
tick a source → change_source (sidebar.py)
                 ├─ updates reader_state
                 └─ update_news() → show_news.refresh() → list is rebuilt
```

`@ui.refreshable` marks a part of the page that can be rebuilt by calling `.refresh()`. There are three: `show_news`, `show_sources` and `show_updated_time`, all in `app.py`.

## Things that look unusual

- **`async` / `await`:** downloading takes seconds. `await run.io_bound(...)` runs the download in the background and lets the screen keep working, instead of freezing until it's done.
- **`lambda entry=entry: open_reader(entry)`:** in a loop, `entry=entry` saves *this* loop's entry. Without it, every button would open the last article.
- **`.classes("...")`:** styling words from Tailwind, e.g. `text-sm` (small text), `opacity-60` (faded), `gap-3` (space between items).
- **`.props("...")`:** settings for the underlying Quasar components, e.g. `flat` (no background), `dense` (compact), `outlined`.
- **`ui.timer`:** runs a function later or repeatedly: once to load the news when the page opens, every minute for "Updated x min ago", and every 5 minutes to check for stale news.

## Changing the look

| You want to... | Change |
|---|---|
| A different main colour | `primary_colour` of your theme in `themes.py` |
| Wider/narrower reading panel | `width=640` in `build_reader_drawer` (`reader_panel.py`) |
| Wider/narrower news column | `max-w-3xl` in `app.py` (try `max-w-2xl` or `max-w-4xl`) |
| Bigger article text | `.reader-text` in your theme's CSS in `themes.py` |
| Highlight colour | `mark { ... }` in your theme's CSS in `themes.py` |
