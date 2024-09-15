from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group  # Import Group model
import logging

# Get the CustomUser model
CustomUser = get_user_model()


class CustomUserModelTest(TestCase):
    def setUp(self):
        """
        Create a test user that we can use in the test cases.
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="testuser@example.com"
        )

    def test_custom_user_creation(self):
        """
        Test that a CustomUser instance can be created successfully.
        """
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_string_representation(self):
        """
        Test the __str__ method of the CustomUser model.
        """
        self.assertEqual(str(self.user), "testuser")

    def test_user_group_permissions(self):
        """
        Test the ManyToMany relationship for groups and permissions.
        """
        # Check if the user has no groups or permissions initially
        self.assertEqual(self.user.groups.count(), 0)
        self.assertEqual(self.user.user_permissions.count(), 0)
        # Add a group or permission to test the relationship
        group = Group.objects.create(name="Test Group")  # Create and add a group
        self.user.groups.add(group)
        self.assertEqual(self.user.groups.count(), 1)
        self.assertIn(group, self.user.groups.all())
