"""
    Management app testing module.
"""
# - Django Modules
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# - Models
from .models import Employee, Plot
from schedule.models import Event


class ManagementPageTestCase(TestCase):
    """
    Testing management view..
    """

    def setUp(self):
        self.username = "armstrongl"
        self.password = "OhWhenTheSaints"
        self.admin = User.objects.create_user(
            username=self.username, password=self.password, is_staff=True
        )

    def test_management_staff(self):
        """
        Management access by staff user

        Condition:
        -----------
        *User is logged AND is staff

        Assertion:
        ----------
        * Request returns 200 (access granted)
        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(reverse("dashboard"))
        request = self.client.get(reverse("management:management"))
        self.assertEqual(request.status_code, 200)

    def test_management_user(self):
        """
        Management access by standard user

        Condition:
        -----------
        *User is logged AND NOT staff

        Assertion:
        ----------
        * Request returns 302 (access denied, redirection)
        *Redirected to dashboard page
        """
        self.admin.is_staff = False
        self.admin.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(reverse("management:management"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/dashboard/")

    def test_management_anonymous(self):
        """
        Management access by external user

        Condition:
        -----------
        *User IS NOT logged in

        Assertion:
        ----------
        * Request returns 302 (access denied, redirection)
        *Redirected to login page
        """
        self.client.logout()
        request = self.client.get(reverse("management:management"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/authentication/login/?next=/management/")


class AddEmployeeTestCase(TestCase):
    """
    Testing employee adding to the database
    """

    def setUp(self):
        self.username = "benningtonc"
        self.first_name = "Chester"
        self.last_name = "Bennington"
        self.password = "1MoreLight"
        self.email = "linkinpark@underground.ht"
        self.phone_number = "0102030405"
        self.address = "20, Wastelands"

        self.user_name = "hayashiy"
        self.pass_word = "ArtOfLife"
        self.user = User.objects.create_user(
            username=self.user_name, password=self.pass_word, is_staff=False
        )
        self.init_user_count = User.objects.count()
        self.init_emp_count = Employee.objects.count()

    def test_add_employee_not_logged(self):
        """
        An external user try to add an employee

        Condition:
        -----------
        *User IS NOT logged in

        Assertion:
        ----------
        * No new User nor Employee
        * Request returns 302 (access denied, redirection)
        * Redirected to login page
        """
        self.client.logout()
        request = self.client.post(
            reverse("management:add_employee"),
            {
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEquals(self.init_emp_count, Employee.objects.count())
        self.assertEquals(self.init_user_count, User.objects.count())
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request, "/authentication/login/?next=/management/add_employee"
        )

    def test_add_employee_not_staff(self):
        """
        An non staff user try to add an employee

        Condition:
        -----------
        *User IS logged in BUT IS NOT staff

        Assertion:
        ----------
        * No new User nor Employee
        * Request returns 403 (forbidden)
        """
        self.client.login(username=self.user_name, password=self.pass_word)
        request = self.client.post(
            reverse("management:add_employee"),
            {
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEquals(request.status_code, 403)
        self.assertEquals(self.init_emp_count, Employee.objects.count())
        self.assertEquals(self.init_user_count, User.objects.count())

    def test_add_employee_staff(self):
        """
        An staff user try to add an employee

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * One new User and Employee
        * Request returns 302 (access denied, redirection)
        """
        self.client.logout()
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.user_name, password=self.pass_word)
        request = self.client.post(
            reverse("management:add_employee"),
            {
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(request.status_code, 302)
        self.assertEquals(self.init_emp_count + 1, Employee.objects.count())
        self.assertEquals(self.init_user_count + 1, User.objects.count())

    def test_add_employee_error(self):
        """
        An staff user try to add an employee with a mistake in form

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * No new User nor Employee
        """
        request = self.client.post(
            reverse("management:add_employee"),
            {
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
                "password1": self.password,
                "password2": "HybridTheory",
            },
        )
        self.assertEquals(self.init_emp_count, Employee.objects.count())
        self.assertEquals(self.init_user_count, User.objects.count())


class AddPlotTestCase(TestCase):
    """
    Testing plot adding to the database
    """

    def setUp(self):
        # - Form fields
        self.variety = "Grenache Noir"
        self.area = "150 pieds"
        self.comment = "A grand besoin d'être traitée contre la cochenille"
        self.plowed = False
        self.watered = False
        self.sulphated = True

        # - User
        self.username = "jaggerm"
        self.password = "SympathyForTheDevil"
        self.user = User.objects.create_user(
            username=self.username, password=self.password, is_staff=False
        )

        # - Base data
        self.init_plot_count = Plot.objects.count()

    def test_add_plot_not_logged(self):
        """
        An external user try to add a plot

        Condition:
        -----------
        *User IS NOT logged in

        Assertion:
        ----------
        * No new Plot
        * Request returns 302 (access denied, redirection)
        * Redirected to login page
        """
        self.client.logout()
        request = self.client.post(
            reverse("management:add_plot"),
            {
                "variety": self.variety,
                "area": self.area,
                "comment": self.comment,
                "plowed": self.plowed,
                "watered": self.watered,
                "sulphated": self.sulphated,
            },
        )
        self.assertEquals(self.init_plot_count, Plot.objects.count())
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request, "/authentication/login/?next=/management/add_plot"
        )

    def test_add_plot_not_staff(self):
        """
        An non staff user try to add a plot

        Condition:
        -----------
        *User IS logged in BUT IS NOT staff

        Assertion:
        ----------
        * No new plot
        * Request returns 403 (forbidden)
        """
        self.client.login(username=self.username, password=self.password)
        request = self.client.post(
            reverse("management:add_plot"),
            {
                "variety": self.variety,
                "area": self.area,
                "comment": self.comment,
                "plowed": self.plowed,
                "watered": self.watered,
                "sulphated": self.sulphated,
            },
        )
        self.assertEquals(request.status_code, 403)
        self.assertEquals(self.init_plot_count, Plot.objects.count())

    def test_add_plot_staff(self):
        """
        An staff user try to add a plot.

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * One new Plot
        * Request returns 302 (redirection)
        """
        self.client.logout()
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.post(
            reverse("management:add_plot"),
            {
                "variety": self.variety,
                "area": self.area,
                "comment": self.comment,
                "plowed": self.plowed,
                "watered": self.watered,
                "sulphated": self.sulphated,
            },
        )
        self.assertEqual(request.status_code, 302)
        self.assertEquals(self.init_plot_count + 1, Plot.objects.count())

    def test_add_plot_error(self):
        """
        An staff user try to add an plot with a mistake in form

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * No new Plot
        """
        request = self.client.post(
            reverse("management:add_plot"),
            {
                "variety": "",
                "area": self.area,
                "comment": self.comment,
                "plowed": self.plowed,
                "watered": self.watered,
                "sulphated": self.sulphated,
            },
        )
        self.assertEquals(self.init_plot_count, Plot.objects.count())


class AddEventTestCase(TestCase):
    """
    Testing event adding to the database
    """

    def setUp(self):

        # - Admin User
        self.username = "jaggerm"
        self.password = "SympathyForTheDevil"
        self.user = User.objects.create_user(
            username=self.username, password=self.password, is_staff=False
        )
        # - Employee
        self.employee = Employee.objects.create(
            username="bulsaraf",
            first_name="Farrokh",
            last_name="Bulsara",
            password="Und3rPressure",
            email="freddie@mercury.uk",
            phone_number="0102030405",
            address="8 in Heaven",
        )

        # - Plot
        self.plot = Plot.objects.create(
            variety="Grenache Noir",
            area="150 pieds",
            comment="A grand besoin d'être traitée contre la cochenille",
            plowed=False,
            watered=False,
            sulphated=True,
        )

        # - Form fields
        self.f_employee = self.employee
        self.f_plot = self.plot
        self.day = "Lundi"
        self.start = "8:00"
        self.end = "10:00"
        self.occupation = "Things to do"

        # - Base data
        self.init_event_count = Event.objects.count()

    def test_add_event_not_logged(self):
        """
        An external user try to add a event

        Condition:
        -----------
        *User IS NOT logged in

        Assertion:
        ----------
        * No new event
        * Request returns 302 (access denied, redirection)
        * Redirected to login page
        """
        self.client.logout()
        request = self.client.post(
            reverse("management:add_event"),
            {
                "employee": self.f_employee,
                "plot": self.f_plot,
                "day": self.day,
                "star": self.start,
                "end": self.end,
                "occupation": self.occupation,
            },
        )
        self.assertEquals(self.init_event_count, Event.objects.count())
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request, "/authentication/login/?next=/management/add_event"
        )

    def test_add_event_not_staff(self):
        """
        An non staff user try to add a event

        Condition:
        -----------
        *User IS logged in BUT IS NOT staff

        Assertion:
        ----------
        * No new event
        * Request returns 403 (forbidden)
        """
        self.client.login(username=self.username, password=self.password)
        request = self.client.post(
            reverse("management:add_event"),
            {
                "employee": self.f_employee,
                "plot": self.f_plot,
                "day": self.day,
                "star": self.start,
                "end": self.end,
                "occupation": self.occupation,
            },
        )
        self.assertEquals(request.status_code, 403)
        self.assertEquals(self.init_event_count, Event.objects.count())

    def test_add_event_staff(self):
        """
        An staff user try to add a event.

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * One new event
        * Request returns 302 (redirection)
        """
        self.client.logout()
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.post(
            reverse("management:add_event"),
            {
                "employee": self.f_employee.id,
                "plot": self.f_plot.id,
                "day": self.day,
                "start": self.start,
                "end": self.end,
                "occupation": self.occupation,
            },
        )
        self.assertEqual(request.status_code, 302)
        self.assertEquals(self.init_event_count + 1, Event.objects.count())

    def test_add_event_error(self):
        """
        An staff user try to add an Event with a mistake in form

        Condition:
        -----------
        *User IS logged in AND IS staff

        Assertion:
        ----------
        * No new Event
        """
        request = self.client.post(
            reverse("management:add_event"),
            {
                "employee": self.f_employee,
                "plot": self.f_plot,
                "day": self.day,
                "start": self.start,
                "end": self.end,
                "occupation": self.occupation,
            },
        )
        self.assertEquals(self.init_event_count, Event.objects.count())
