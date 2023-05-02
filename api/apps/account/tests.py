from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.testconf import UserFactory, AccountFactory, TransactionFactory
from api.apps.account.models import Account
from api.apps.account.serializers import AccountSerializer


class AccountViewsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_authenticated_user_can_list_own_accounts(self):
        account = AccountFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], account.name)

    def test_authenticated_user_can_create_new_account(self):
        data = {"name": "New Account", "currency_code": "CAD", "kind": "spending"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("accounts-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Account.objects.filter(user=self.user, name=data["name"]).exists()
        )

    def test_user_only_views_own_accounts(self):
        AccountFactory()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_access_view(self):
        response = self.client.get(reverse("accounts-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_nonexistent_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing_account(self):
        account = AccountFactory(user=self.user)
        data = {"name": "Updated Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("accounts-detail", kwargs={"pk": account.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_update_account_with_invalid_data(self):
        data = {"name": ""}
        account = AccountFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("accounts-detail", kwargs={"pk": account.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_delete_existing_account(self):
        account = AccountFactory(user=self.user)
        self.assertEqual(Account.objects.count(), 1)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("accounts-detail", kwargs={"pk": account.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

    def test_delete_non_existing_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("accounts-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_balance_computes_sum_of_transactions(self):
        account = AccountFactory(user=self.user, initial_balance=0)
        transaction1 = TransactionFactory(user=self.user, account=account, amount=100)
        transaction2 = TransactionFactory(user=self.user, account=account, amount=1.55)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            float(account.balance), transaction1.amount + transaction2.amount
        )


class AccountSerializerTests(APITestCase):
    def test_contains_instance_expected_fields(self):
        account = AccountFactory()
        serializer = AccountSerializer(instance=account)
        data = serializer.data
        self.assertEqual(
            list(data.keys()),
            ["id", "name", "kind", "currency_code", "balance", "initial_balance"],
        )
        self.assertEqual(data["name"], account.name)

    def test_contains_data_expected_fields(self):
        data = {"name": "New Account", "currency_code": "CAD", "kind": "spending"}
        serializer = AccountSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], data["name"])
        self.assertEqual(serializer.data["kind"], data["kind"])
