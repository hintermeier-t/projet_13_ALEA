"""
This modulz contains the FeedEntry class which stores needed data from
an RSS feed.
"""


class FeedEntry:
    """
    The FeedEntry class will be used to format the data collected from the
        RSS feed articles.
    
    Attributes:
    -----------
    :self.date (string): article's publishing date;
    :self.title (string): title of the article;
    :self.url (string): url to the complete article;
    :self.thumbnail_url (string): link to the attached picture;
    :self.summary (string): summary that will be displayed.
    """
    def __init__(self, date, title, summary, link, img):
        self.date = date
        self.title = title
        self.url = link
        self.thumbnail_url = img
        self.summary = summary
