from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.testconf import UserFactory, CategoryFactory
from api.apps.category.models import Category
from api.apps.category.serializers import CategorySerializer


class CategoryViewsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_authenticated_user_can_list_categories(self):
        category = CategoryFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], category.name)

    def test_authenticated_user_can_create_category(self):
        data = {"name": "New Category", "detailed_name": "Test Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("categories"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Category.objects.filter(user=self.user, name=data["name"]).exists()
        )

    def test_user_only_views_public_categories(self):
        CategoryFactory()
        category = CategoryFactory(user=None)
        self.assertEqual(len(Category.objects.all()), 2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], category.name)

    def test_user_only_views_own_categories(self):
        CategoryFactory()
        category = CategoryFactory(user=self.user)
        self.assertEqual(len(Category.objects.all()), 2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], category.name)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_authenticated_user_cannot_create_category_with_invalid_data(self):
        data = {"name": "", "description": "Test Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("categories"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_unauthenticated_user_cannot_list_categories(self):
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_category(self):
        data = {"name": "New Category", "description": "Test Name"}
        response = self.client.post(reverse("categories"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_category_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_category_valid_cid(self):
        category = CategoryFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("category", kwargs={"cid": category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], category.name)

    def test_update_category_valid_data(self):
        category = CategoryFactory(user=self.user)
        data = {"name": "Updated Category"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("category", kwargs={"cid": category.id}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["detailed_name"], category.detailed_name)

    def test_handles_invalid_data_in_patch_request(self):
        category = CategoryFactory(user=self.user)
        data = {"name": "", "detailed_name": "Test Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse("category", kwargs={"cid": category.id}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_retrieve_category_invalid_cid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("category", kwargs={"cid": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_owner_can_access_cid(self):
        category = CategoryFactory()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("category", kwargs={"cid": category.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_valid_cid(self):
        category = CategoryFactory(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("category", kwargs={"cid": category.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_delete_category_invalid_cid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("category", kwargs={"cid": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategorySerializerTests(APITestCase):
    def test_contains_instance_expected_fields(self):
        category = CategoryFactory()
        serializer = CategorySerializer(instance=category)
        data = serializer.data
        self.assertEqual(
            list(data.keys()),
            ["id", "name", "detailed_name", "user"],
        )
        self.assertEqual(data["name"], category.name)

    def test_contains_data_expected_fields(self):
        data = {"name": "New Category", "detailed_name": "Test Name"}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data["name"], data["name"])
        self.assertEqual(serializer.data["detailed_name"], data["detailed_name"])
