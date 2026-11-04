# feeds

Getting the news in. Nothing in here draws anything on screen.

| File | What it does | Main function |
|---|---|---|
| `fetch.py` | Skips sources that are still placeholders, downloads the rest (8 at a time, so it's quick), cleans Google Alerts ones, and reports any that failed. Also opens feed files such as `sample_feeds/`. | `load_all_feeds(news_sources)` → `(all_feeds, failed_source_names)` |
| `clean.py` | Tidies Google Alerts entries: removes HTML tags, turns `&#39;` into `'`, turns `<br>` into spaces, and swaps Google's redirect link for the real article link. | `clean_google_alert_feeds(parsed_feeds)` |
| `news_store.py` | Holds the latest downloaded news in one shared place, and knows when it's out of date. | `news_store.refresh()`, `news_store.is_out_of_date(minutes)` |
| `full_text.py` | Downloads an article's web page and pulls out just the article text, using the **trafilatura** library. | `fetch_full_article_text(link)` |
| `details.py` | Lists which keys (pieces of information) a feed's entries have. Used by `explore_feed_keys.py`. | `find_entry_keys(parsed_feed)` |

## How the pieces connect

```
news_store.refresh
 └─ load_all_feeds
     ├─ parse_news_feeds           → downloads all feeds at the same time
     └─ clean_google_alert_feeds   → only the Google Alerts ones
```

## Good to know

- **Why a store?** Without it, every window (or every website visitor) would download every feed again. The store downloads once and everyone shares the result until it's older than `REFRESH_MINUTES`.
- **`NewsStore` is a class.** A class bundles data (the news, when it was downloaded) with the functions that work on it (`refresh`, `is_out_of_date`). `self` inside the class means "this store".
- **Downloading in parallel:** `ThreadPoolExecutor` runs several downloads at once, because most of the time is spent waiting for websites to reply. Ten feeds take about as long as the slowest one, not all ten added together.
- **Full text is remembered:** `@lru_cache` means opening the same article twice only downloads it once. It also remembers failures, so a blocked site isn't retried until the app restarts.
- **Glued-together words?** Check `clean_html_text` in `clean.py`: it's the one place HTML is turned into text.
