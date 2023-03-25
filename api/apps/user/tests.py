from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


class TestUsersManagers(TestCase):
    def test_create_user(self):
        User = get_user_model()
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
        User = get_user_model()
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
