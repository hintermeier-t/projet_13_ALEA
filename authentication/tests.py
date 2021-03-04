"""
    Authentication app testing module.
"""
from django.test import TestCase
from django.urls import reverse


# - Index page
class IndexPageTestCase(TestCase):
    """
    Testing index view.
    """

    # - Index page returns 200
    def test_index_page(self):
        """
        Accessing index view.

        Returns 200.
        """
        request = self.client.get(reverse("index"))
        self.assertEqual(request.status_code, 200)