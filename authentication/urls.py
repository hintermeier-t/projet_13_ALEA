from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.account, name="account"),
    path(
        "password_reset_query", views.password_reset_query, name="password_reset_query"
    ),
    path("forgotten_password", views.forgotten_password, name="forgotten_password"),
    path(
        "password_reset/(<uidb64>/<usr_token>/",
        views.password_reset,
        name="password_reset",
    ),
    path("password_change", views.password_change, name="password_change"),
]

app_name = "authentication"
