# search

Filters entries down to those that mention the search terms. Nothing in here draws anything on screen.

| File | Function | What it does |
|---|---|---|
| `search.py` | `split_search_text` | `"Nvidia, oil"` → `["nvidia", "oil"]` |
| | `entry_contains_term` | Does one entry's headline or summary contain a term? Whole words only, any case. |
| | `entry_matches_search` | Does an entry match *any* term (or *all* terms, if Match all is on)? |
| | `filter_entries_by_search` | Keeps the matching entries. With an empty search box, keeps everything. |

## Good to know

- **Whole words:** `\b` in the pattern means "word edge", so `oil` matches "oil" but not "soil". To allow part-word matches, remove the two `\b`s in `entry_contains_term`.
- **Any vs all:** `any([True, False])` is `True`; `all([True, False])` is `False`. That one line in `entry_matches_search` is the whole difference.
- **What gets searched:** headline and summary. To search more, change the `searchable_text` line in `entry_contains_term`.
- Highlighting the matches on screen is done separately, in `gui/formatting.py`.
