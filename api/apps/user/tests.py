from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserViewsTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@company.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "FakePassword",
        }

    def test_register_with_email_verification(self):
        response = self.client.post(reverse("user-list"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(user.is_active, False)

        # Parse email to retrieve activation URL
        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [line for line in email_lines if "/activate/" in line][0]
        activation_url = activation_link.split("/testserver", 1)[1]

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(user.is_active, True)

    def test_unverified_user_cannot_access_info(self):
        response = self.client.get(reverse("user-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
