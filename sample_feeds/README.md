# sample_feeds

Three small RSS files full of **made-up stories**, so the app has something to show the first time you run it. None of the companies, people or events in them are real.

They're listed in `settings/feeds.py` under **"Sample feeds (delete me)"**. Once you've added your own feeds, delete that group (and this folder, if you like).

They also show that a feed "URL" can be a file path. That's handy for testing: save any RSS feed as an `.xml` file here and point a source at it, e.g. `"My test feed": "sample_feeds/my-test.xml"`.

The dates are fixed, so after a few days the stories will show as older ("28 Oct" instead of "3 h ago").
