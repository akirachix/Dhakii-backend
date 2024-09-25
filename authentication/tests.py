from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group  # Import Group model
from django.core.exceptions import ValidationError

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


class CustomUserUnhappyPathTest(TestCase):
    def test_custom_user_creation_without_username(self):
        """
        Unhappy path: Test that creating a user without a username raises a ValidationError.
        """
        user = CustomUser(
            email="userwithoutusername@example.com",
            password="password123",
            username=None,  # No username provided
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Trigger validation for missing username

    def test_custom_user_creation_with_invalid_email(self):
        """
        Unhappy path: Test that creating a user with an invalid email format raises a ValidationError.
        """
        user = CustomUser(
            email="invalid-email",  # Invalid email format
            username="invalidemailuser",
            password="password123",
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Trigger validation for invalid email

    def test_custom_user_creation_with_existing_email(self):
        """
        Unhappy path: Test that creating a user with a duplicate email raises a ValidationError.
        """
        CustomUser.objects.create_user(
            email="existinguser@example.com",
            username="existinguser",
            password="password123",
        )
        user = CustomUser(
            email="existinguser@example.com",  # Duplicate email
            username="newuser",
            password="password123",
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Trigger validation for duplicate email

    def test_custom_user_creation_without_email(self):
        """
        Unhappy path: Test that creating a user without an email raises a ValidationError.
        """
        user = CustomUser(
            email=None, username="nouser", password="password123"  # No email provided
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Trigger validation for missing email

    def test_custom_user_creation_with_blank_password(self):
        """
        Unhappy path: Test that creating a user with a blank password raises a ValueError.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="blankpassworduser@example.com",
                username="blankpassworduser",
                password="",  # Blank password
            )


def test_user_without_permissions_fails(self):
    """
    Unhappy path: Test that a user with invalid permissions raises a ValidationError.
    """
    user = CustomUser(
        email="invalidpermissions@example.com",
        username="invalidpermissionsuser",
        password="password123",
    )
    user.save()  
    user.user_permissions.clear()  
    with self.assertRaises(ValidationError):
        user.full_clean()  
