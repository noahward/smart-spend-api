from django.urls import reverse
from rest_framework import status
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase

from api.apps.user.models import User


class UserManagersTests(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="regular@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.assertEqual(user.email, "regular@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(
                email="super@user.com",
                password="foo",
                first_name="bar",
                last_name="baz",
                is_superuser=False,
            )


class UserViewsTests(APITestCase):
    def test_register(self):
        url = reverse("register")
        data = {
            "email": "register@user.com",
            "password": "foo",
            "first_name": "bar",
            "last_name": "baz",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, data["email"])
        self.assertEqual(response.data["profile"]["email"], data["email"])
        self.assertIn("key", response.data["token"])
        self.assertIn("expiry", response.data["token"])

    def test_login_correct_credentials(self):
        User.objects.create_user(
            email="login@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.assertTrue(self.client.login(email="login@user.com", password="foo"))
        url = reverse("login")
        data = {"email": "login@user.com", "password": "foo"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["email"], data["email"])
        self.assertIn("key", response.data["token"])
        self.assertIn("expiry", response.data["token"])

    def test_login_bad_credentials(self):
        User.objects.create_user(
            email="login@user.com",
            password="invalid",
            first_name="bar",
            last_name="baz",
        )
        self.assertTrue(self.client.login(email="login@user.com", password="invalid"))
        url = reverse("login")
        data = {"email": "login@user.com", "password": "foo"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Invalid credentials")

    def test_main_user(self):
        user = User.objects.create_user(
            email="main@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.client.force_authenticate(user)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "main@user.com")
