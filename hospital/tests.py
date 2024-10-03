from django.test import TestCase
from django.contrib.auth import get_user_model
from community_health_promoter.models import CHP
from hospital.models import Hospital


class HospitalModelTest(TestCase):
    def setUp(self):
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Set up an example Hospital instance
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            type="General",
            village="Test Village",
            hospital_location="Test Location",
            sub_location="Test Sub-location",
        )

        # Set up a valid CHP instance, providing a user
        self.chp = CHP.objects.create(
            user=self.user,  # Pass the created user here
            registered_date="2023-01-01",
            reg_no="CHP001",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )

    def test_hospital_creation(self):
        # Test if the Hospital instance was created successfully
        self.assertEqual(self.hospital.name, "Test Hospital")
        self.assertEqual(self.hospital.type, "General")
        self.assertEqual(self.hospital.village, "Test Village")
        self.assertEqual(self.hospital.hospital_location, "Test Location")
        self.assertEqual(self.hospital.sub_location, "Test Sub-location")
        self.assertIsNotNone(
            self.hospital.created_at
        )  # Ensure auto_add fields are populated
        self.assertIsNotNone(self.hospital.updated_at)

    def test_hospital_str_method(self):
        # Test the __str__ method
        expected_str = f"{self.hospital.name} {self.hospital.hospital_location}"
        self.assertEqual(str(self.hospital), expected_str)
