from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Index page view.
    """
    context = {}
    return render(request, "authentication/index.html", context)