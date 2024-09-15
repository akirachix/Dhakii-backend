from django.test import TestCase
from django.contrib.auth import get_user_model
from nurse.models import Nurse
from hospital.models import Hospital


class NurseModelTest(TestCase):
    def setUp(self):
        # Create a user instance with an email
        self.user = get_user_model().objects.create_user(
            username="nurseuser", email="nurseuser@example.com", password="password123"
        )

        # Create a hospital instance using the correct field name (e.g., 'address' instead of 'location')
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            hospital_location="123 Test Street",  # Use 'address' if that's the correct field name
        )

        # Create a nurse instance
        self.nurse = Nurse.objects.create(
            user=self.user,
            hospital_id=self.hospital,
            gender="Female",
            tel_no="+254712345678",
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )

    def test_nurse_creation(self):
        # Test if the Nurse instance was created successfully
        self.assertEqual(self.nurse.user, self.user)
        self.assertEqual(self.nurse.hospital_id, self.hospital)
        self.assertEqual(self.nurse.tel_no, "+254712345678")
