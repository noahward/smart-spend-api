import factory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.testconf import USER_PASSWORD, UserFactory
from api.apps.user.models import User
from api.apps.user.serializers import UserSerializer


class UserViewsTests(APITestCase):
    def test_register_succeeds(self):
        data = {
            "email": "testuser@company.com",
            "password": USER_PASSWORD,
            "first_name": factory.Faker("first_name"),
            "last_name": factory.Faker("last_name"),
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn("profile", response.data)
        self.assertIn("token", response.data)
        self.assertIn("key", response.data["token"])
        self.assertIn("expiry", response.data["token"])
        self.assertEqual(response.data["profile"]["email"], data["email"])

    def test_register_fails_bad_email(self):
        data = {
            "email": "invalid_email",
            "password": USER_PASSWORD,
            "first_name": factory.Faker("first_name"),
            "last_name": factory.Faker("last_name"),
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("email", response.data)

    def test_register_fails_missing_field(self):
        data = {
            "email": "testuser@company.com",
            "password": USER_PASSWORD,
            "first_name": "",
            "last_name": factory.Faker("last_name"),
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("first_name", response.data)

    def test_register_fails_duplicate_email(self):
        user = UserFactory()
        self.assertEqual(User.objects.count(), 1)
        data = {
            "email": user.email,
            "password": USER_PASSWORD,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"][0], "user with this email address already exists."
        )
        self.assertEqual(User.objects.count(), 1)

    def test_login_succeeds(self):
        user = UserFactory()
        data = {"email": user.email, "password": USER_PASSWORD}
        url = reverse("login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("profile", response.data)
        self.assertIn("token", response.data)
        self.assertIn("key", response.data["token"])
        self.assertIn("expiry", response.data["token"])
        self.assertEqual(response.data["profile"]["email"], data["email"])

    def test_login_bad_credentials(self):
        user = UserFactory()
        data = {"email": user.email, "password": "foo"}
        url = reverse("login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Invalid credentials")

    def test_retrieve_main_user_when_authenticated(self):
        user = UserFactory()
        self.client.force_authenticate(user)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            list(response.data.keys()), ["id", "email", "first_name", "last_name"]
        )
        self.assertEqual(response.data["email"], user.email)

    def test_retrieve_main_user_when_unauthenticated_fails(self):
        UserFactory()
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_retrieve_only_owned_data(self):
        user = UserFactory()
        UserFactory()
        self.client.force_authenticate(user)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(User.objects.count(), 2)


class UserSerializerTests(APITestCase):
    def test_contains_instance_expected_fields(self):
        user = UserFactory()
        serializer = UserSerializer(instance=user)
        data = serializer.data
        self.assertEqual(list(data.keys()), ["id", "email", "first_name", "last_name"])
        self.assertEqual(data["email"], user.email)

    def test_contains_data_expected_fields(self):
        data = {
            "email": "testuser@company.com",
            "password": USER_PASSWORD,
            "first_name": "first",
            "last_name": "last",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["email"], data["email"])
        self.assertEqual(serializer.data["first_name"], data["first_name"])
        self.assertEqual(serializer.data["last_name"], data["last_name"])
