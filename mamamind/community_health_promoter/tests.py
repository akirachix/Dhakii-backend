from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model  # Import the User model
from community_health_promoter.models import (
    CHP,
)  # Adjust this import based on your app's structure


class CHPModelTest(TestCase):
    def setUp(self):
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Set up an example CHP instance, providing the user object
        self.chp = CHP.objects.create(
            user=self.user,  # Pass the entire user object here, NOT the ID
            registered_date=timezone.now().date(),
            reg_no="CHP123",
            phone_number="1234567890",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )

    def test_chp_creation(self):
        # Test if the CHP instance was created successfully
        self.assertEqual(self.chp.reg_no, "CHP123")
        self.assertEqual(self.chp.phone_number, "1234567890")
        self.assertEqual(self.chp.location, "Test Location")
        self.assertEqual(self.chp.sub_location, "Test Sub-location")
        self.assertEqual(self.chp.village, "Test Village")

    def test_chp_str_method(self):
        # Test the __str__ method
        expected_str = f"{self.chp.reg_no} - {self.chp.user.username}"  # Use the username from the related user
        self.assertEqual(str(self.chp), expected_str)
