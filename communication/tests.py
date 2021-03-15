"""
    Communication app's tests
"""

# - Django modules
from django.test import TestCase
from django.urls import reverse

# - Custom models
from .models import Message
from management.models import Employee


class MessageViewTestCase(TestCase):
    """
        Internal Messenger testing class.

    Attributes (setUp method) :
    ---------------------------
    :self.username (string): Employee's username used for connection;
    :self.password (string): Employee's password used for connection;
    :self.employee (Employee): Employee object. Will try to read and send
        messages;
    :self.message (Message): A Message already saved in the DB;
    :self.count (int): Number of saved messaged at the beginning.
    """

    def setUp(self):
        # - Employee
        self.username = "sirkisn"
        self.password = "Station13"
        self.employee = Employee.objects.create_user(
            username=self.username,
            first_name="Nicola",
            last_name="Sirkis",
            password=self.password,
            email="alice@june.indo",
            phone_number="0102030405",
            address="40, Belfast",
        )
        # - Message
        self.message = Message.objects.create(
            employee=self.employee,
            content="A nos célébrations !",
            date="2020-05-26 10:00",
        )
        self.count = Message.objects.count()

    def test_chat_access_not_logged_in(self):
        """
        A non logged user wants to read the messages.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertion:
        ----------
        *   Status code 302 (redirect);
        *   Redirected to login page.
        """

        self.client.logout()
        request = self.client.get(reverse("communication:chat"))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request, "/authentication/login/?next=/communication/")

    def test_chat_access_logged_in(self):
        """
        A logged user wants to read the messages.

        Condition:
        ----------
        *   User IS logged in.

        Assertion:
        ----------
        *   Status code 200 (OK);
        *   The message is displayed.
        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(reverse("communication:chat"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.context["messages"]), 1)
        self.assertEqual(
            request.context["messages"][0].content, "A nos célébrations !")

    def test_chat_send_not_logged_in(self):
        """
        A non logged user try to send a message.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertion:
        ----------
        *   Status code 302 (redirect);
        *   Redirected to login page.

        """

        self.client.logout()
        request = self.client.post(
            reverse("communication:chat"), {
                "content": "J'ai demandé à la Lune"}
        )
        self.assertEqual(request.status_code, 302)
        self.assertEqual(Message.objects.count(), self.count)

    def test_chat_send_logged_in(self):
        """
        A logged user try to senda message.

        Condition:
        ----------
        *   User IS logged in.

        Assertion:
        ----------
        *   Status code 200 (OK);
        *   The new message is saved;
        *   There are 2 messages displayed;
        *   The messages are the first one and the new one,
            in the right order (Oldest -> Newest).
        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.post(
            reverse("communication:chat"), {"content": "Un été français"}
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Message.objects.count(), self.count + 1)
        self.assertEqual(len(request.context["messages"]), 2)
        self.assertEqual(
            request.context["messages"][0].content, "A nos célébrations !")
        self.assertEqual(
            request.context["messages"][1].content, "Un été français")


class DeleteMessageTestCase(TestCase):
    """
        Delete message function testing class.

    Attributes (setUp method) :
    ---------------------------
    :self.username (string): User's username used for connection;
    :self.password (string): User's password used for connection;
    :self.employee (Employee): Employee object. Author of the messages;
    :self.user (Employee): Employee object. Will try to delete a message;
    :self.message (Message): A Message already saved in the DB;
    :self.message (Message): Another Message already saved in the DB;
    :self.count (int): Number of saved messaged at the beginning.
    """

    def setUp(self):

        # - Employee who sent the messages
        self.employee = Employee.objects.create_user(
            username="younga",
            first_name="Angus",
            last_name="Young",
            password="Pow3rage",
            email="backinblack80@ac.dc",
            phone_number="0102030405",
            address="The Razor's Edge",
        )

        # - The user
        self.username = "chedidm"
        self.password = "MamaS4m"
        self.user = Employee.objects.create_user(
            username=self.username,
            first_name="Matthieu",
            last_name="Chédid",
            password=self.password,
            email="jedis@ime.m",
            phone_number="0102030405",
            address="Presqu'Il",
            is_staff=False,
        )

        # - Two messages
        self.message = Message.objects.create(
            employee=self.employee,
            content="You've been thunderstruck",
            date="1990-09-10 10:00",
        )

        self.another = Message.objects.create(
            employee=self.employee,
            content="In rock we trust, it's rock or bust",
            date="2014-11-17 10:00",
        )

        # - Data count
        self.count = Message.objects.count()

    def test_delete_not_logged_in(self):
        """
        A non logged user try to delete an message.

        Condition:
        ----------
        *   User IS NOT logged in.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No message deleted.

        """

        self.client.logout()
        request = self.client.get(
            reverse("communication:delete", kwargs={"id": self.message.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/communication/delete/"
            + str(self.message.id)
            + "/",
        )
        self.assertEqual(self.count, Message.objects.count())

    def test_delete_not_staff(self):
        """
        A non staff user try to delete an message.

        Condition:
        ----------
        *   User IS logged in but NOT staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to staff login page;
        *   No message deleted.

        """

        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("communication:delete", kwargs={"id": self.message.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(
            request,
            "/backoffice/login/?next=/communication/delete/"
            + str(self.message.id)
            + "/",
        )
        self.assertEqual(self.count, Message.objects.count())

    def test_delete_staff(self):
        """
        A staff user try to delete a message.

        Condition:
        ----------
        *   User IS logged in AND IS staff.

        Assertions:
        -----------
        *   Status code = 302 (redirects);
        *   User is redirected to communication;
        *   One message deleted;
        *   The right message has been deleted.

        """

        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        request = self.client.get(
            reverse("communication:delete", kwargs={"id": self.message.id})
        )
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, "/communication/")
        self.assertEqual(self.count - 1, Message.objects.count())
        self.assertEqual(
            Message.objects.all()[0].content,
            "In rock we trust, it's rock or bust"
        )
