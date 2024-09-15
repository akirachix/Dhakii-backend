from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        """
        Set up initial test data.
        """
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            user_role="nurse",
        )

    def test_user_creation(self):
        """
        Test that a user can be created successfully.
        """
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(self.user.user_role, "nurse")

    def test_superuser_creation(self):
        """
        Test that a superuser can be created and has the correct attributes.
        """
        admin_user = User.objects.create_superuser(
            email="admin@example.com", username="adminuser", password="adminpass"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.email, "admin@example.com")

    def test_user_without_email_fails(self):
        """
        Test that creating a user without an email raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", username="nouser", password="password123"
            )

    def test_user_string_representation(self):
        """
        Test the __str__ method of the User model.
        """
        self.assertEqual(str(self.user), "testuser")

    def test_user_role_assignment(self):
        """
        Test that the user role can be assigned correctly.
        """
        self.assertEqual(self.user.user_role, "nurse")
        # Change role and test again
        self.user.user_role = "admin"
        self.user.save()
        self.assertEqual(self.user.user_role, "admin")


class UserModelUnhappyPathTest(TestCase):
    def test_user_creation_without_username(self):
        """
        Unhappy path: Test that creating a user without a username raises an error.
        """
        with self.assertRaises(ValidationError):
            user = User(
                email="userwithoutusername@example.com",
                username=None,  # No username provided
                password="password123",
            )
            user.full_clean()  # This triggers model validation

    def test_user_creation_with_invalid_email(self):
        """
        Unhappy path: Test that creating a user with an invalid email format raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            user = User(
                email="invalid-email",  # Invalid email format
                username="invalidemailuser",
                password="password123",
            )
            user.full_clean()  # This should raise a ValidationError for invalid email

    def test_user_creation_with_existing_email(self):
        """
        Unhappy path: Test that creating a user with an existing email raises an IntegrityError.
        """
        User.objects.create_user(
            email="existinguser@example.com",
            username="existinguser",
            password="password123",
        )
        with self.assertRaises(ValidationError):
            user = User(
                email="existinguser@example.com",  # Duplicate email
                username="newuser",
                password="password123",
            )
            user.full_clean()  # This should raise a ValidationError for duplicate email

    def test_user_creation_without_role(self):
        """
        Unhappy path: Test that creating a user without a role raises a ValidationError.
        """
        user = User(
            email="noroleuser@example.com",
            username="noroleuser",
            password="password123",
            user_role=None,  # No user role assigned
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # This should raise a ValidationError

    def test_user_creation_with_invalid_role(self):
        """
        Unhappy path: Test that creating a user with an invalid role raises a ValidationError.
        """
        user = User(
            email="invalidroleuser@example.com",
            username="invalidroleuser",
            password="password123",
            user_role="invalidrole",  # Invalid role
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # This should raise a ValidationError for invalid role


def test_user_without_password_fails(self):
    """
    Unhappy path: Test that creating a user without a password raises an error.
    """
    with self.assertRaises(ValueError):
        User.objects.create_user(
            email="nopassworduser@example.com", username="nopassworduser", password=None
        )
