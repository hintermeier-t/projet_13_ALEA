from django.test import TestCase
from django.urls import reverse

from . import rss
from .views import rss_reader

# Create your tests here.


class RssReaderPageTestCase(TestCase):
    def test_rssreader_page(self):
        """
        Accessing rss reader view.

        Assertions:
        -----------
        * 'rssreader' view returns a list
        * The list contains 5 items
        * Each entry is a FeedEntry class object
        """
        entries = rss_reader()
        self.assertTrue(isinstance(entries, list))
        self.assertEqual(len(entries), 5)
        for entry in entries:
            self.assertTrue(isinstance(entry, rss.FeedEntry))
