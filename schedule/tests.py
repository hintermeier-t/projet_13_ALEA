"""
    Schedule app's tests.
"""

# - Django modules
from django.test import TestCase
from django.urls import reverse

# - Models
from .models import Event
from management.models import Employee, Plot


class PlanningPageTestCase(TestCase):
    """
    Test class of the display_planning view.

    Attributes:
    -----------

    :self.employee (Employee): Used to create an event and connect;
    :self.s_employee (Employee): an witness Employee;
    :self.plot (Plot): Used to create an event;
    :self.event (Event): Uderzo's event to be displayed.
    :self.s_event (Event): Goscinny's event not to be displayed.
    """

    def setUp(self):

        # - Employees set up
        self.employee = Employee.objects.create(
            username="uderzoa",
            first_name="Albert",
            last_name="Uderzo",
            password="Les12Trav0",
            email="asterix@legaulois.fr",
            phone_number="0102030405",
            address="Petibonum",
        )

        self.s_employee = Employee.objects.create(
            username="goscinnyr",
            first_name="René",
            last_name="Goscinny",
            password="LeC0upDuMenh1r",
            email="obelix@jesuispasgros.fr",
            phone_number="0102030405",
            address="Babaorum",
        )

        # - Plot set up
        self.plot = Plot.objects.create(
            variety="Grenache Noir",
            area="150 pieds",
            comment="A grand besoin d'être traitée contre la cochenille",
            plowed=False,
            watered=False,
            sulphated=True,
        )

        # - Events set up
        self.event = Event.objects.create(
            employee=self.employee,
            plot=self.plot,
            day="Lundi",
            start="8:00",
            end="12:00",
            occupation="Taille des sarments",
        )

        self.event = Event.objects.create(
            employee=self.s_employee,
            plot=self.plot,
            day="Mardi",
            start="8:00",
            end="12:00",
            occupation="Goûter le raisin",
        )

    def test_display_not_logged_in(self):
        """
        A non logged user wants to access schedule.

        Condition:
        -----------
        *   User IS NOT logged in

        Assertions:
        -----------
        *   request returns 302 (redirects)
        *   Redirects to the login page
        """

        self.client.logout()
        request = self.client.get(reverse("schedule:planning"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/authentication/login/?next=/schedule/")

    def test_display_logged_in(self):
        """
        A user wants to know his schedule.

        Condition:
        -----------
        *   User IS logged in

        Assertions:
        -----------
        *   request returns 200 (OK)
        *   context contains 1 event
        *   the event is the good one
        """
        self.client.force_login(self.employee)

        request = self.client.get(reverse("schedule:planning"))
        self.assertEqual(len(request.context["events"]), 1)
        self.assertEqual(request.context["events"][0].day, "Lundi")
        self.assertEqual(request.context["events"]
                         [0].occupation, "Taille des sarments")
