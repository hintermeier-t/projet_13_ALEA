"""
    Authentication app's views.
"""

# - Django modules
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

# - Custom modules and models
from news.views import rss_reader
from news.rss import FeedEntry


def index(request):
    """
    Index page view.
    """
    context = {}
    return render(request, "authentication/index.html", context)


def login_view(request):
    """
        Login page.

        Redirects on "dashboard" page after login
            (or if user already logged in);
        Renders signin page with form if not logged in, with form error if
            invalid.

    """
    form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("dashboard")

    return render(request, "authentication/login.html", {"form": form})


@login_required
def logout_view(request):
    """
        Logout view.

        End user's connection.
    """
    logout(request)
    return redirect("index")


@login_required
def dashboard(request):
    """
        Dashboard view.
        Leads to the central page of the app. Gather weather intel
            (client-side), and News from the "Chambre de l'Agriculture".
    """

    entries = rss_reader()
    context = {"entries": entries}
    return render(request, "authentication/dashboard.html", context)
