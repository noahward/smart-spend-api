from datetime import date

import factory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.testconf import UserFactory, AccountFactory, TransactionFactory
from api.apps.transaction.models import Transaction


class TransactionListDetailViewsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.account = AccountFactory(user=self.user)
        self.transaction_data = {
            "date": date.today(),
            "description": factory.Faker("catch_phrase"),
            "currency_code": "CAD",
            "amount": 100,
            "account": self.account.id,
        }

    def test_authenticated_user_can_create_new_transaction(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("transaction-list"), self.transaction_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Transaction.objects.filter(
                user=self.user, description=self.transaction_data["description"]
            ).exists()
        )

    def test_authenticated_user_can_list_own_transactions(self):
        transaction = TransactionFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("transaction-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["description"], transaction.description)

    def test_user_only_views_own_transactions(self):
        TransactionFactory()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("transaction-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_user_cannot_access_view(self):
        response = self.client.get(reverse("transaction-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_nonexistent_transaction(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("transaction-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing_transaction(self):
        data = {"description": "Updated Description"}
        transaction = TransactionFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("transaction-detail", kwargs={"pk": transaction.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], data["description"])

    def test_update_transaction_with_invalid_data(self):
        data = {"description": ""}
        transaction = TransactionFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("transaction-detail", kwargs={"pk": transaction.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_delete_existing_account(self):
        transaction = TransactionFactory(user=self.user)
        self.assertEqual(Transaction.objects.count(), 1)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("transaction-detail", kwargs={"pk": transaction.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_delete_non_existing_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("transaction-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
