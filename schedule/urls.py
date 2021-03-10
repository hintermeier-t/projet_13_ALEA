# - Django modules
from django.conf import settings
from django.urls import path, include

# - Views
from . import views

urlpatterns = [
    path("", views.display_planning, name="planning")
]

app_name = "schedule"
