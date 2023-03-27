from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.testconf import UserFactory, AccountFactory
from api.apps.account.models import Account
from api.apps.account.serializers import AccountSerializer


class AccountViewsTests(APITestCase):
    def test_authenticated_user_can_list_own_accounts(self):
        user = UserFactory()
        account = AccountFactory(user=user)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], account.name)

    def test_authenticated_user_can_create_new_account(self):
        user = UserFactory()
        data = {"name": "New Account", "kind": "spending"}
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse("accounts"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Account.objects.filter(user=user, name=data["name"]).exists())

    def test_user_only_views_own_accounts(self):
        user1 = UserFactory()
        user2 = UserFactory()
        AccountFactory(user=user1)
        self.client.force_authenticate(user=user2)
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_access_view(self):
        response = self.client.get(reverse("accounts"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_nonexistent_account(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("account", kwargs={"aid": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing_account(self):
        user = UserFactory()
        account = AccountFactory(user=user)
        data = {"name": "Updated Name"}
        self.client.force_authenticate(user=user)
        response = self.client.patch(
            reverse("account", kwargs={"aid": account.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["nickname"], account.nickname)

    def test_update_account_with_invalid_data(self):
        user = UserFactory()
        account = AccountFactory(user=user)
        data = {"name": ""}
        self.client.force_authenticate(user=user)
        response = self.client.patch(
            reverse("account", kwargs={"aid": account.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_delete_existing_account(self):
        user = UserFactory()
        account = AccountFactory(user=user)
        self.assertEqual(Account.objects.count(), 1)
        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse("account", kwargs={"aid": account.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

    def test_delete_non_existing_account(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse("account", kwargs={"aid": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AccountSerializerTests(APITestCase):
    def test_contains_instance_expected_fields(self):
        account = AccountFactory()
        serializer = AccountSerializer(instance=account)
        data = serializer.data
        self.assertEqual(
            list(data.keys()),
            ["id", "name", "nickname", "kind", "balance", "initial_balance"],
        )
        self.assertEqual(data["name"], account.name)

    def test_contains_date_expected_fields(self):
        data = {"name": "New Account", "kind": "spending"}
        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], data["name"])
        self.assertEqual(serializer.data["kind"], data["kind"])
