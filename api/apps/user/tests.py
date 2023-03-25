from django.urls import reverse
from rest_framework import status
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase

from api.apps.user.models import User
from api.apps.user.serializers import (
    UserSerializer,
    LoginUserSerializer,
    CreateUserSerializer,
)


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
        self.assertEqual(list(response.data.keys()), ["profile", "token"])
        self.assertEqual(list(response.data["token"].keys()), ["key", "expiry"])
        self.assertEqual(response.data["profile"]["email"], data["email"])

    def test_login_good_credentials(self):
        User.objects.create_user(
            email="login@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.assertTrue(self.client.login(email="login@user.com", password="foo"))
        url = reverse("login")
        data = {"email": "login@user.com", "password": "foo"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["profile", "token"])
        self.assertEqual(list(response.data["token"].keys()), ["key", "expiry"])
        self.assertEqual(response.data["profile"]["email"], data["email"])

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
        self.assertEqual(list(response.data.keys()), ["non_field_errors"])
        self.assertEqual(response.data["non_field_errors"][0], "Invalid credentials")

    def test_main_user(self):
        user = User.objects.create_user(
            email="main@user.com", password="foo", first_name="bar", last_name="baz"
        )
        self.client.force_authenticate(user)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            list(response.data.keys()), ["id", "email", "first_name", "last_name"]
        )
        self.assertEqual(response.data["email"], "main@user.com")


class UserSerializersTests(APITestCase):
    def test_contains_expected_fields(self):
        user = User.objects.create_user(
            email="main@user.com", password="foo", first_name="bar", last_name="baz"
        )
        serializer = UserSerializer(instance=user)
        data = serializer.data
        self.assertEqual(list(data.keys()), ["id", "email", "first_name", "last_name"])
        self.assertEqual(data["email"], "main@user.com")

    def test_create_user_valid_input(self):
        data = {
            "email": "register@user.com",
            "first_name": "bar",
            "last_name": "baz",
            "password": "foo",
        }
        serializer = CreateUserSerializer()
        user = serializer.create(data)
        serialized_user = serializer.to_representation(user)
        self.assertEqual(serialized_user["email"], data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_create_user_missing_data(self):
        serializer = CreateUserSerializer()
        data = {"email": "register@user.com", "first_name": "bar", "password": "foo"}
        with self.assertRaises(KeyError):
            serializer.create(data)

    def test_create_user_existing_email(self):
        serializer = CreateUserSerializer()
        data1 = {
            "email": "register@user.com",
            "first_name": "bar",
            "last_name": "baz",
            "password": "foo",
        }
        data2 = {
            "email": "register@user.com",
            "first_name": "bar",
            "last_name": "baz",
            "password": "foo",
        }
        serializer.create(data1)
        with self.assertRaises(IntegrityError):
            serializer.create(data2)

    def test_valid_credentials(self):
        User.objects.create_user(
            email="login@user.com", password="foo", first_name="bar", last_name="baz"
        )
        data = {"email": "login@user.com", "password": "foo"}
        serializer = LoginUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_credentials(self):
        data = {"email": "absent@user.com", "password": "wrongpassword"}
        serializer = LoginUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_invalid_email(self):
        data = {"email": "invalidemail", "password": "foo"}
        serializer = LoginUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_empty_password(self):
        data = {"email": "login@user.com", "password": ""}
        serializer = LoginUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
