from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.management_view, name="management"),
    path("add_plot", views.add_plot, name="add_plot"),
    path("add_employee", views.add_employee, name="add_employee"),
    path("add_event", views.add_event, name="add_event"),
]

app_name = "management"
