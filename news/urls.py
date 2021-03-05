from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path("rssreader/", views.rss_reader, name="rssreader"),
]

app_name = "news"