from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.apps.user.models import User
from api.apps.account.models import Account
from api.apps.account.serializers import AccountSerializer


class AccountViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="regular@user.com", password="foo", first_name="bar", last_name="baz"
        )

    def test_authenticated_user_can_list_own_accounts(self):
        self.client.force_authenticate(user=self.user)
        Account.objects.create(user=self.user, name="Test Account")
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Test Account")

    def test_authenticated_user_can_create_new_account(self):
        data = {"name": "New Account", "kind": "spending"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("accounts"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Account.objects.filter(user=self.user, name="New Account").exists()
        )

    def test_unauthenticated_user_cannot_access_view(self):
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_accesses_nonexistent_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("account", kwargs={"aid": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_serializer_validation_and_deserialization_logic(self):
        data = {"name": "New Account", "kind": "spending"}
        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], data["name"])
        self.assertEqual(serializer.data["kind"], data["kind"])

    def test_user_creates_account_with_invalid_data(self):
        data = {"name": "New Account", "kind": ""}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("accounts"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Account.objects.filter(user=self.user, name="New Account").exists()
        )
