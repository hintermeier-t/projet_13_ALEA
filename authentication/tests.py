"""
    Authentication app testing module.
"""
# - Django Modules
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# - Selenium modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

# - Index page
class IndexPageTestCase(TestCase):
    """
    Testing index view.
    """

    # - Index page returns 200
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
            username = self.username, password = self.password
        )
        

    # - test login view with invalid credentials
    def test_login_invalid_credentials(self):
        """
        Conditions:
        -----------
        *User send wrong password ("ImInLoveWithMyCar" != "BohemianRhapsody").

        Assertions:
        -----------
        *Status code = 200 (we can access login page);
        *User is not authenticated after post
        """
        request = self.client.post(
            reverse("authentication:login"),
            {"username": self.username, "password": "ImInLoveWithMyCar"},
        )
        self.assertEqual(request.status_code, 200)
        self.assertFalse(request.context["user"].is_authenticated)
        
    # - test login view with valid credentials
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
    
    

    # - Test logout view
    def test_logout(self):
        """
        Conditions:
        -----------
        *User is logged in.

        Assertions:
        -----------
        *Status code = 302 (redirection)
        *Redirect page = index (after logout)
        """
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(reverse("authentication:logout"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/")
