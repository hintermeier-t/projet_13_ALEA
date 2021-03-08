"""alea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from authentication import views as auth

urlpatterns = [
    #Admin Site: only for Dev
    path('backoffice/', admin.site.urls),
    #Authentication app
    path("authentication/", include("authentication.urls", namespace="authentication")),
    path("", auth.index, name="index"),
    path("dashboard/", auth.dashboard, name="dashboard"),
    #Management app
    path("management/", include("management.urls", namespace="management")),
    #Schedule app
    path("schedule/", include("schedule.urls", namespace="schedule")),
    #Communication app
    path("communication/", include("communication.urls", namespace="communication")),
    #News App
    path("news/", include("news.urls", namespace="news")),
    
]
