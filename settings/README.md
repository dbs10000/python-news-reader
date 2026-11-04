# settings

The control panel. Everything you're likely to want to change, without touching any logic, lives here.

| File | What it holds |
|---|---|
| `feeds.py` | `FEED_GROUPS`: your news sources, in groups. Each group becomes a heading in the sidebar. **This is the file to edit first.** |
| `app_settings.py` | How the app runs (website or desktop window), its design (`THEME`), how often it refreshes, and the sidebar's starting choices. |
| `entry_details.py` | Friendly names for the pieces of information feeds contain. Used by `explore_feed_keys.py`. |

## Adding your feeds

`feeds.py` starts with two placeholder sources and a group of made-up sample feeds:

```python
FEED_GROUPS = {
    "My feeds": {
        "My first feed": PLACEHOLDER_URL,      # ← replace PLACEHOLDER_URL with "https://..."
        "My second feed": PLACEHOLDER_URL,
    },
    "Sample feeds (delete me)": { ... },
}
```

1. Replace `PLACEHOLDER_URL` with a feed URL in quotes, e.g. `"https://feeds.bbci.co.uk/news/rss.xml"`, and rename the source.
2. Add more lines, or more groups, in the same pattern.
3. Delete the sample group when you no longer need it.
4. Restart the app.

Sources left as `PLACEHOLDER_URL` show in the sidebar as **not set up** and are skipped. Google Alerts feeds are spotted by their URL and cleaned automatically. See [`docs/ADDING_FEEDS.md`](../docs/ADDING_FEEDS.md) for where to find feeds.

## Other common changes

| You want to... | In `app_settings.py` |
|---|---|
| Change the design | `THEME = "ink"`, `"frost"`, `"signal"` or `"classic"` (preview first with `?theme=frost` on the web address) |
| Open in its own window instead of the browser | `APP_MODE = ...` default `"website"` → `"desktop"` (needs pywebview) |
| Start in the Headlines view, or with 10 per source | `DEFAULT_VIEW_MODE`, `DEFAULT_ENTRIES_PER_SOURCE` |
| Refresh more or less often | `REFRESH_MINUTES` |

`APP_MODE` reads `os.environ.get("APP_MODE", "website")`, which means "use APP_MODE if a hosting service has set one, otherwise website". The same file works on your computer and online without editing.
