# Adding feeds

The app reads **RSS feeds**: simple, machine-readable lists of a website's latest articles. Most news sites, blogs and podcasts have one. Each feed you add becomes a source in the sidebar.

## 1. Find a feed

### From a website

- Look for an **RSS** link or the orange RSS icon, often in the footer or on a "Subscribe" page.
- Try adding `/rss`, `/feed` or `/rss.xml` to the end of the site's address.
- Search for "*site name* RSS feed".

A few well-known public feeds to try:

| Source | Feed URL |
|---|---|
| BBC News | `https://feeds.bbci.co.uk/news/rss.xml` |
| BBC Technology | `https://feeds.bbci.co.uk/news/technology/rss.xml` |
| The Guardian (UK) | `https://www.theguardian.com/uk/rss` |
| Hacker News (front page) | `https://hnrss.org/frontpage` |

Websites change their feeds from time to time. If one shows as **failed** in the sidebar, check the address in a browser.

### From Google Alerts (any topic you like)

Google Alerts can turn any search into a feed, so you can follow a topic rather than a website.

1. Go to [google.com/alerts](https://www.google.com/alerts) and type a search, for example `"data engineer apprenticeship" London`.
2. Click **Show options** and set **Deliver to** to **RSS feed**. Setting **How many** to *All results* is also useful.
3. Click **Create Alert**, then click the **RSS icon** next to it and copy the address.

Search tips:
- Use quotes to keep a phrase together: `"supply chain"`.
- `OR` (in capitals) matches either word: `nvidia OR amd`.
- Use a minus sign to leave words out: `apprenticeship -senior`.
- `site:` limits results to one website: `site:gov.uk apprenticeship`.

The app spots Google Alerts feeds by their address and tidies them up automatically. It removes the bold tags and odd symbols, and swaps Google's redirect links for the real article links.

> **Keep Google Alerts links private.** They're personal links to your account's alerts. If you put this project on GitHub, don't commit your real feed URLs: keep them in a copy of `settings/feeds.py` that you don't upload, or make the repository private.

## 2. Add it to the app

Open `settings/feeds.py` and replace a placeholder:

```python
    "My feeds": {
        "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
        "Data apprenticeships": "https://www.google.com/alerts/feeds/...",
    },
```

You can make as many groups as you like. Each group becomes a heading in the sidebar:

```python
FEED_GROUPS = {
    "World news": {
        "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
        "The Guardian": "https://www.theguardian.com/uk/rss",
    },
    "Career": {
        "Data apprenticeships": "https://www.google.com/alerts/feeds/...",
    },
}
```

Restart the app (Ctrl+C in the terminal, then `uv run main.py` again) and your sources appear in the sidebar.

## 3. See what a feed contains (optional)

Different feeds include different information: some have images, authors or categories. To see everything a feed offers, run:

```
uv run explore_feed_keys.py
```

This prints a table for each feed in the terminal: every key, whether the app uses it, and an example value.
