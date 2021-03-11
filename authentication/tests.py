"""
    Authentication app testing module.
"""
# - Built-in module
import re

# - Django Modules
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


# - Selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

# - Custom models
from management.models import Employee

# - Index page
class IndexPageTestCase(TestCase):
    """
    Testing index view.
    """

    def test_index_page(self):
        """
        Accessing index view.

         Assertion:
        -----------
        Returns 200.
        """
        request = self.client.get(reverse("index"))
        self.assertEqual(request.status_code, 200)


class LoginLogoutTestCase(TestCase):
    """
    Testing login and logout views.

    Attributes (setUp method) :
    ---------------------------
    :self.username (string): username field used to connect and create User
        object;
    :self.password (string): password field used to connect and create User
        object;
    :self.user (User): Django's User object.
    :self.driver (webdriver): Selenium's webdriver

    Tests:
    ------
    :test_login_invalid_credentials(self): Request a connection with wrong
        credentials (here password);
    :test_login_valid_credentials(self): Request a connection with right
        credentials.
    :test_logout(self): Request a Logout from the app
    """

    def setUp(self):
        """
        Tests setup
        """

        self.username = "mercuryf"
        self.password = "BohemianRhapsody"
        User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_login_invalid_credentials(self):
        """
        Conditions:
        -----------
        *User send wrong password ("ImInLoveWithMyCar" != "BohemianRhapsody").

        Assertions:
        -----------
        *Status code = 200 (we can access login page);
        *User IS NOT authenticated after post
        """
        request = self.client.post(
            reverse("authentication:login"),
            {"username": self.username, "password": "ImInLoveWithMyCar"},
        )
        self.assertEqual(request.status_code, 200)
        self.assertFalse(request.context["user"].is_authenticated)

    def test_login_valid_credentials(self):
        """
        Conditions:
        -----------
        *All conditions are OK.

        Assertions:
        -----------
        *Status code = 302 (redirection after connection);
        *Redirection page = dashboard.
        """
        request = self.client.post(
            reverse("authentication:login"),
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/dashboard/")

    def test_logout(self):
        """
        Conditions:
        -----------
        *User IS logged in.

        Assertions:
        -----------
        *Status code = 302 (redirection)
        *Redirect page = index (after logout)
        """
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(reverse("authentication:logout"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/")

class PasswordResetTestCase(TestCase):
    """
    Testing password reset function.

    Attributes (setUp method) :
    ---------------------------
    :self.username (string): username field used to connect and create User
        object;
    :self.password (string): password field used to connect and create User
        object;
    :self.user (User): Django's User object.
    """

    def setUp(self):
        # - Employee
        self.username = "marsb"
        self.password = "24KMagic"
        self.employee = Employee.objects.create_user(
            username = self.username,
            first_name = "Bruno",
            last_name = "Mars",
            password = self.password,
            email = "unothodox@jukebox.com",
            phone_number = "0102030405",
            address = "24, Silk Sonic Road",
        )
        self.new_password = "LeaveTheD00rOpen"

    def test_forgotten_password(self):
        """
        A user queries a new password.

        Assertion:
        ----------
        *   Returns 200 (OK).
        """
        request = self.client.get(
            reverse('authentication:forgotten_password')
        )
        self.assertEqual(request.status_code, 200)

    def test_reset_mail_send(self):
        """
        A user send a password reset request.

        Assertion:
        ----------
        *   No mail sent before;
        *   Returns 200 (OK);
        *   A message is displayed;
        *   A mail is sent;
        *   The mail has the right subject;
        """

        self.assertEqual(len(mail.outbox), 0)

        request = self.client.post(
            reverse("authentication:password_reset_query"),
            {
                "username": self.username,
            }
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.context['message'],
        "Un e-mail vient de vous être envoyé. Consultez votre boîte mails")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "ALEA :Vous avez demandé un nouveau mot de passe"
        )
    def test_force_password_change(self):
        """
        A non user try to force change password.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertion:
        ----------
        *   Request returns 302;
        *   Redirection to login page.
        """

        self.client.logout()
        request = self.client.post(
            reverse("authentication:password_change"),
            {'password' : self.new_password}
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/authentication/login/?next=/authentication/password_change"
        )

    def test_password_change(self):
        """
        A user changes his password.

        Condition:
        ----------
        *   User IS logged in.

        Assertion:
        ----------
        *   Request returns 302;
        *   Redirection to dashboard page.
        """
        self.client.login(
            username = self.username,
            password = self.password
        )
        request = self.client.post(
            reverse("authentication:password_change"),
            {'password' : self.new_password}
        )
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, "/dashboard/")
