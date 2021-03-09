"""
This modul contains the FeedEntry class which stores needed data from
an RSS feed.
"""


class FeedEntry:
    def __init__(self, date, title, summary, link, img):
        self.date = date
        self.title = title
        self.url = link
        self.thumbnail_url = img
        self.summary = summary
