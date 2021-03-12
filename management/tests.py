"""
    Management app testing module.
"""

# - Built-in module
import datetime

# - Django Modules
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# - Models
from .models import Employee, Plot
from schedule.forms import EventCreationForm
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
        self.assertRedirects(request, "/backoffice/login/?next=/management/")

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
        self.assertRedirects(request, "/backoffice/login/?next=/management/")


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
            request, "/backoffice/login/?next=/management/add_employee"
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
        self.assertEquals(request.status_code, 302)
        self.assertRedirects(
            request, "/backoffice/login/?next=/management/add_employee"
        )
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

    Attributes:
    -----------
    :self.variety (string): Plot variety field;
    :self.area (string): Plot area field;
    :self.comment (string): Plot comment field;
    :self.plowed (bool): Plot variety field;
    :self.watered (bool): Plot variety field;
    :self.sulphated (bool): Plot variety field;
    :self.username (string): User's data;
    :self.password(string): User's password;
    :self.user (User): User that will try to use add view;
    :self.init_plot_count (int): Initial plot number.

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
            request, "/backoffice/login/?next=/management/add_plot")

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
        self.assertEquals(request.status_code, 302)
        self.assertRedirects(
            request, "/backoffice/login/?next=/management/add_plot")
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
        self.employee = Employee.objects.create_user(
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
            request, "/backoffice/login/?next=/management/add_event")

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
        self.assertEquals(request.status_code, 302)
        self.assertRedirects(
            request, "/backoffice/login/?next=/management/add_event")
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
        A staff user try to add an Event with a mistake in form

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


class DeleteObjectTestCase(TestCase):
    """
    Delete view tests. The view can delete either an employee, a plot or
    an event.
    """

    def setUp(self):
        # - The employee to delete
        self.employee = Employee.objects.create_user(
            username="saarestom",
            first_name="Marko",
            last_name="Saaresto",
            password="Carnival0fRust",
            email="poetsofthe@fall.com",
            phone_number="0102030405",
            address="Cauldron Lake lodge",
        )

        # - The user
        self.username = "bellamym"
        self.password = "R3sistance"
        self.user = Employee.objects.create_user(
            username=self.username,
            first_name="Matthew",
            last_name="Bellamy",
            password=self.password,
            email="simulation@theory.uk",
            phone_number="0102030405",
            address="Supermassive Black Hole",
            is_staff=False,
        )

        # - The plot to delete
        self.plot = Plot.objects.create(
            variety="Muscat",
            area="12 hectares",
            comment="A gelé",
            plowed=True,
            watered=True,
            sulphated=True,
        )

        # - The event to delete
        self.event = Event.objects.create(
            employee=self.employee,
            plot=self.plot,
            day="Vendredi",
            start="10:00",
            end="12:00",
            occupation="Goûter le vin",
        )
        # - Count data
        self.count_emp = Employee.objects.count()
        self.count_plot = Plot.objects.count()
        self.count_event = Event.objects.count()

    def test_delete_employee_not_logged_in(self):
        """
        A non logged user try to delete an employee

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No employee deleted.

        """

        self.client.logout()
        request = self.client.get(
            reverse(
                "management:delete",
                kwargs={"model": "employee", "id": self.employee.id},
            )
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/employee/"
            + str(self.employee.id)
            + "/",
        )
        self.assertEqual(self.count_emp, Employee.objects.count())

    def test_delete_plot_not_logged_in(self):
        """
        A non logged user try to delete a plot.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No plot deleted.

        """

        self.client.logout()
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "plot", "id": self.plot.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/plot/"
            + str(self.plot.id)
            + "/",
        )
        self.assertEqual(self.count_plot, Plot.objects.count())

    def test_delete_event_not_logged_in(self):
        """
        A non logged user try to delete an event.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No event deleted.

        """

        self.client.logout()
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "event", "id": self.event.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/event/"
            + str(self.event.id)
            + "/",
        )
        self.assertEqual(self.count_event, Event.objects.count())

    def test_delete_emp_not_staff(self):
        """
        A non staff user try to delete an employee.

        Condition:
        ----------
        *   User IS logged in AND NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No employee deleted.

        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse(
                "management:delete",
                kwargs={"model": "employee", "id": self.employee.id},
            )
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/employee/"
            + str(self.employee.id)
            + "/",
        )
        self.assertEqual(self.count_emp, Employee.objects.count())

    def test_delete_plot_not_staff(self):
        """
        A non staff user try to delete a plot.

        Condition:
        ----------
        *   User IS logged in AND NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No plot deleted.

        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "plot", "id": self.plot.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/plot/"
            + str(self.plot.id)
            + "/",
        )
        self.assertEqual(self.count_plot, Plot.objects.count())

    def test_delete_event_not_staff(self):
        """
        A non staff user try to delete an event.

        Condition:
        ----------
        *   User IS logged in AND NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No event deleted.

        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "event", "id": self.event.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/delete/event/"
            + str(self.event.id)
            + "/",
        )
        self.assertEqual(self.count_event, Event.objects.count())

    def test_delete_event_staff(self):
        """
        A staff user try to delete an event.

        Condition:
        ----------
        *   User IS logged in AND IS staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to management;
        *   One event deleted.

        """

        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "event", "id": self.event.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/management/")
        self.assertEqual(self.count_event - 1, Event.objects.count())

    def test_delete_plot_staff(self):
        """
        A staff user try to delete a plot.

        Condition:
        ----------
        *   User IS logged in AND IS staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to management;
        *   One plot deleted.

        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("management:delete", kwargs={
                    "model": "plot", "id": self.plot.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/management/")
        self.assertEqual(self.count_plot - 1, Plot.objects.count())

    def test_delete_emp_staff(self):
        """
        A staff user try to delete an employee.

        Condition:
        ----------
        *   User IS logged in AND IS staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to management;
        *   One employee deleted.

        """

        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse(
                "management:delete",
                kwargs={"model": "employee", "id": self.employee.id},
            )
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/management/")
        self.assertEqual(self.count_emp - 1, Employee.objects.count())

class EditTestCase(TestCase):
    """
    Testing data editing by admin.

    Attributes:
    -----------
    :self.plot (Plot): Plot to modify;
    :self.employee (Employee): Employee to modify;
    :self.user (Employee): User who will try to edit data;
    self.username (string): User's username;
    self.password (string): User's password;
    :self.event (Event): Event to modify.
    """

    def setUp(self):
        
        # - Employee
        self.employee = Employee.objects.create(
            username="letissierh",
            first_name="Heloise",
            last_name="Letissier",
            password="Christine&TheQu33ns",
            email="nuit17@52.fr",
            phone_number="0102030405",
            address="Paradis Perdu",
        )

        # - User
        self.username = "desplata"
        self.password = "0Dark30"
        self.user = Employee.objects.create_user(
            username = self.username,
            first_name = "Alexandre",
            last_name  ="Desplat",
            password = self.password,
            email = "deathlyh@llows.fr",
            phone_number = "0102030405",
            address = "Isle of Dogs",
            is_staff = False,
        )

        # - Plot
        self.plot = Plot.objects.create(
            variety = "Chardonnay",
            area = "325 pieds",
            comment = "-",
            plowed = True,
            watered = True,
            sulphated = True,
        )

        # - Event
        self.event = Event.objects.create(
            employee = self.employee,
            plot = self.plot,
            day = "Lundi",
            start = "18:00",
            end = "20:00",
            occupation = "Sarclage"
        )

    def test_access_edit_not_logged_in(self):
        """
        A non logged user try to access edit forms.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        """

        self.client.logout()
        request = self.client.get(
            reverse("management:edit",
            kwargs={"model": "employee", "id": self.employee.id},)
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/edit/employee/"
            + str(self.employee.id)
            + "/"
        )

    def test_save_edit_not_logged(self):
        """
        A non logged user try to change data.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   Employee still has original data.
        """
        self.client.logout()
        request = self.client.post(
            reverse("management:save",
            kwargs={"model": "employee", "id": self.employee.id}),
            {
                'username' : self.username,
                'first_name' : "John",
                'last_name' : "Williams",
                'password' : self.password,
                'email' : self.employee.email,
                'phone_number' : self.employee.phone_number,
                'address' : "In a Galaxy Far Away",
                'is_staff' : True, 
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/save/employee/"
            + str(self.employee.id)
            + "/"
        )
        self.assertFalse(self.employee.is_staff)
        self.assertEqual(self.employee.first_name, "Heloise")
        self.assertEqual(self.employee.last_name, "Letissier")
        self.assertEqual(self.employee.address, "Paradis Perdu")

    def test_access_edit_not_staff(self):
        """
        A non staff user try to access edit forms.

        Condition:
        ----------
        *   User IS logged in AND NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        """

        self.client.login(
            username = self.username,
            password = self.password
        )
        request = self.client.get(
            reverse("management:edit",
            kwargs={"model": "plot", "id": self.plot.id},)
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/edit/plot/"
            + str(self.plot.id)
            + "/"
        )

    def test_save_edit_not_staff(self):
        """
        A non staff user try to change data.

        Condition:
        ----------
        *   User IS logged in AND NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   Plot still has original data.
        """

        self.client.login(
            username = self.username,
            password = self.password
        )
        request = self.client.post(
            reverse("management:save",
            kwargs={"model": "plot", "id": self.plot.id},),
            {
                'variety' : "Chardonnay",
                'area' : "325 pieds",
                'comment' : "-",
                'plowed' : False,
                'watered' : False,
                'sulphated' : False,
            }
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/management/save/plot/"
            + str(self.plot.id)
            + "/"
        )
        self.assertTrue(self.plot.watered)
        self.assertTrue(self.plot.plowed)
        self.assertTrue(self.plot.sulphated)

    def test_access_edit_staff(self):
        """
        A staff user try to access edit forms.

        Condition:
        ----------
        *   User IS logged in AND IS Staff.

        Assertions:
        -----------
        *   Status code = 200 (ok);
        *   Template used is edit.html;
        *   The right edit form is loaded.
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(
            username = self.username,
            password = self.password
        )
        request = self.client.get(
            reverse("management:edit",
            kwargs={"model": "event", "id": self.event.id},)
        )
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, "management/edit.html")
        self.assertEqual(request.context['model'], 'event')
        self.assertEqual(
            type(request.context['form']), 
            type(EventCreationForm())
            )

    def test_access_edit_staff(self):
        """
        A staff user try to change event data.

        Condition:
        ----------
        *   User IS logged in AND IS Staff.

        Assertions:
        -----------
        *   Status code = 302 (Redirects);
        *   Redirected to management page;
        *   A confirmation message is displayed;
        *   The event is correctly modified.
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(
            username = self.username,
            password = self.password
        )
        request = self.client.post(
            reverse(
                "management:save",
                kwargs={"model": "event", "id": self.event.id}
            ),
            {
                'employee' : self.employee.id,
                'plot' : self.plot.id,
                'day' : "Vendredi",
                'start' : "8:00",
                'end' : "12:00",
                'occupation' : "Arrosage",
            }
        )
        self.event.refresh_from_db()
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/management/")
        self.assertEqual(self.client.session['message'],
        'Evénement modifié avec succès')
        self.assertEqual(self.event.day, 'Vendredi')
        self.assertEqual(self.event.start, datetime.time(8, 0))
        self.assertEqual(self.event.end, datetime.time(12, 0))

