from rest_framework.test import APITestCase

from api.testconf import CategoryFactory
from api.apps.category.serializers import CategorySerializer


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
