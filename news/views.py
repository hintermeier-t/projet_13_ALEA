"""
    News app's views
"""
# - Built-in modules
import os

# - Django modules
from django.shortcuts import render

# - Venv modules
import feedparser
import geoip2.database
import requests


# - Custom modules
from .rss import FeedEntry
from .weather import WeatherWidget


def rss_reader():
    """
    RSS reader.

    Gather news from the "Chambre de l'Agriculture" RSS feed, and return
        what needed to the Dashboard (authentication.views).

    """
    entries = []
    news_feed = feedparser.parse(
        "https://chambres-agriculture.fr/flux-rss/flux-rss-actualite/flux.rss"
    )
    small_entries = news_feed.entries[:5]
    for entry in small_entries:
        if len(entry["links"]) < 2:
            img = os.path.relpath(
                "../static/authentication/images/nopicture.png")
        else:
            img = entry["links"][1]["href"]
        entries.append(
            FeedEntry(
                entry["published"],
                entry["title"],
                entry["summary"],
                entry["links"][0]["href"],
                img,
            )
        )
    return entries


def weather_update(ip=""):

    widget = WeatherWidget(ip)
    widget.update()

    return widget
