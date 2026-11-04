# selection

Turns "everything downloaded" into "the articles to show". Nothing in here draws anything on screen.

| File | Function | What it does |
|---|---|---|
| `arrange.py` | `collect_entries_from_sources` | Every entry from the ticked sources, in one list, each labelled with `"source_name"` |
| | `remove_duplicate_entries` | Drops entries with the same link or headline as an earlier one |
| | `simplify_headline` | `"SK Hynix Shares Surge!"` → `"skhynixsharessurge"`, so tiny differences don't stop duplicates matching |
| | `get_entry_datetime` | When an entry was published, as a proper date in UTC |
| | `sort_entries_newest_first` | Newest at the top; undated entries at the bottom |
| | `limit_entries_per_source` | Keeps the first *n* from each source (0 keeps all) |

## The order matters

`gui/app.py` runs them in this order: **collect → remove duplicates → search → sort → limit.**

- Sorting *before* limiting means "5 per source" gives you each source's 5 **newest** articles.
- Searching *before* limiting means "5 per source" while searching for `oil` gives up to 5 *oil* articles from each source, rather than searching only the first 5.
