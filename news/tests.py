"""
    News app's tests
    
    """

# - Django modules
from django.test import TestCase
from django.urls import reverse

# - Custom modules
from . import rss, weather
from .views import rss_reader, weather_update



class RssReaderTestCase(TestCase):
    def test_rssreader_page(self):
        """
        Accessing RSS reader view.

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

class WeatherUpdateTestCase(TestCase):
    def setUp(self):
        self.invalid_ip = "127.0.0.1"
        # - Lyon City hall's website
        self.valid_ip = "176.162.143.16"

    def test_weather_invalid_ip(self):
        """
            Accessing Weather data.

            Condition:
            ----------
            *   IP is not valid (private)

            Assertions:
            -----------
            * 'weather_update' view returns a WeatherWidget object
            * The Wweather returned is about Paris
        """
        request = weather_update(self.invalid_ip)
        self.assertTrue(isinstance(request, weather.WeatherWidget))
        self.assertEqual(
            request.lat,
            '48.866667'
        )
        self.assertEqual(
            request.lon,
            '2.333333'
        )
    def test_weather_without_ip(self):
        """
            Accessing Weather data.

            Condition:
            ----------
            *   IP is not valid (nothing bu an IP address)
            
            Assertions:
            -----------
            * 'weather_update' view returns a WeatherWidget object
            * The Weather returned is about Paris
        """
        request = weather_update("ILoveParis")
        self.assertTrue(isinstance(request, weather.WeatherWidget))
        self.assertEqual(
            request.lat,
            '48.866667'
        )
        self.assertEqual(
            request.lon,
            '2.333333'
        )
        

    def test_weather_valid_ip(self):
        """
            Accessing Weather data.

            Assertions:
            -----------
            * 'weather_update' view returns a WeatherWidget object
            * The Wweather returned is about Normandy
        """
        request = weather_update(self.valid_ip)
        self.assertTrue(isinstance(request, weather.WeatherWidget))
        self.assertEqual(
            request.lat,
            '49.2457'
        )
        self.assertEqual(
            request.lon,
            '1.4236'
        )