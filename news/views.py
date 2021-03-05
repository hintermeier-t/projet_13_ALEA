from django.shortcuts import render

import feedparser
import requests

from . import rss
# Create your views here.
def rss_reader(request):
    entries = []
    news_feed = feedparser.parse(
        "https://chambres-agriculture.fr/flux-rss/flux-rss-actualite/flux.rss"
        )
    small_entries = news_feed.entries[:5]
    for entry in small_entries:
        if len(entry["links"])<2 :
            img = "{% static \'authentication/images/nopicture.png\' %}"
        else :
            img = entry["links"][1]["href"]
        entries.append(
            rss.FeedEntry(
                entry["published"],
                entry["title"],
                entry["summary"],
                entry["links"][0]["href"],
                img
            )
        )
    context = {"entries": entries}
    return entries