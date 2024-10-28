from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from community_health_promoter.models import CHP
from django.core.exceptions import ValidationError

class CHPModelTest(TestCase):
    def setUp(self):
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Set up an example CHP instance, providing the user object
        self.chp = CHP.objects.create(
            user=self.user,  # Pass the entire user object here, NOT the ID
            reg_no="CHP123",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )

    def test_chp_creation(self):
        # Test if the CHP instance was created successfully
        self.assertEqual(self.chp.reg_no, "CHP123")
        self.assertEqual(self.chp.location, "Test Location")
        self.assertEqual(self.chp.sub_location, "Test Sub-location")
        self.assertEqual(self.chp.village, "Test Village")

    def test_chp_str_method(self):
        # Test the __str__ method
        expected_str = f"{self.chp.reg_no} - {self.chp.user.username}"  # Use the username from the related user
        self.assertEqual(str(self.chp), expected_str)

class CHPModelUnhappyPathTest(TestCase):
    def setUp(self):
        # Create a valid User instance for testing
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

    def test_missing_required_fields(self):
        """
        Test creating a CHP instance with missing required fields should raise an error.
        """
        # Test missing 'reg_no' which is required
        chp = CHP(
            user=self.user,
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )
        with self.assertRaises(ValidationError):
            chp.full_clean()  # This should raise a ValidationError because 'reg_no' is missing

    def test_exceeding_max_length(self):
        """
        Test exceeding max_length of fields should raise a validation error.
        """
        chp = CHP(
            user=self.user,
            reg_no="C" * 256,  # Exceeds the max_length of 255
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )
        with self.assertRaises(ValidationError):
            chp.full_clean()  # This should raise a ValidationError due to exceeded max_length

    def test_invalid_user_relationship(self):
        """
        Test creating a CHP instance without a valid user should raise an error.
        """
        chp = CHP(
            user=None,  # User is missing
            reg_no="CHP123",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )
        with self.assertRaises(ValidationError):
            chp.full_clean()  # This should raise a ValidationError because 'user' is required
