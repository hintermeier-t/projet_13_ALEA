"""
    Authentication app's views.
"""

# - Django modules

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# - Venv modules
from ipware import get_client_ip

# - Custom modules and models
from . import token
from management.models import Employee
from news.views import rss_reader, weather_update
from news.rss import FeedEntry



def index(request):
    """
    Index page view.
    """
    context = {
        'title' : 'Application Logistique pour Exploitation Agricole'
    }
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
    context={
        'title' : 'ALEA: Se Connecter',
        'form' : form
    }
    return render(request, "authentication/login.html", context)


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
    ip, is_routable = get_client_ip(request)

    current_weather = weather_update(ip)
    entries = rss_reader()
    context = {
        'entries': entries,
        'weather_data' : current_weather,
        'title': 'ALEA: Tableau de Bord'
    }
    return render(request, "authentication/dashboard.html", context)

@login_required
def account(request):
    """
        Account view.
        Displays the User's data.
    """
    context = {
        'title' : 'ALEA: Mon Compte',
        'employee': Employee.objects.get(
            user_ptr_id= request.user
        ),
        }
    return render(request, "authentication/account.html", context)

def forgotten_password(request):
    context = {
        'title' : "ALEA: Mot de passe oublié"
    }
    
    return render(request, "authentication/forgotten_password.html", context)
    
def password_reset_query(request):

    if request.method == 'POST':
        field = request.POST['username']
        try :
            user = get_object_or_404(Employee, username = field)
        except Http404:
            context = {
                'message': "Aucun utilisateur ne correspond à ce nom d'utilisateur."
            }
            return forgotten_password(request, context)

        current_site = get_current_site(request)
        mail_subject = "ALEA :Vous avez demandé un nouveau mot de passe"
        message = render_to_string(
            'authentication/reset_password.html', 
            {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token.password_token.make_token(user),
            }
        )
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        context = {
            'title': "ALEA: Mot de passe Oublié",
            'message': 'Un e-mail vient de vous être envoyé. Consultez votre boîte mails'
        }
        return render(request,  "authentication/forgotten_password.html", context)
        
def password_reset(request,  uidb64, usr_token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Employee.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        user = None
    if user is not None and token.password_token.check_token(user, usr_token):
        login(request, user)
        context = {
            'title': 'Modification du mot de passe'
        }
        return render(request, "authentication/password_reset.html", context)
    else:
        return render("500.html")

@login_required
def password_change(request):
    if request.method == 'POST':
        new_password = request.POST['password']
        request.user.set_password(new_password)
        request.user.save()
        return redirect('dashboard')