from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

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

    Redirects on "index" page after login (or if user already logged in);
    Renders signin page if not logged in, with error if invalid.

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
    logout(request)
    return redirect("index")


@login_required
def dashboard(request):
    entries = rss_reader()
    context = {"entries": entries}
    return render(request, "authentication/dashboard.html", context)
