from django.test import TestCase
from django.urls import reverse

from . import rss
# Create your tests here.

class RssReaderPageTestCase(TestCase):
    def test_rssreader_page(self):
        """
        Accessing rss reader view.

        Returns 200.
        """
        request = self.client.get(reverse("news:rssreader"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.context["entries"]), 5)