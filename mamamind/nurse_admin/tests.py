from django.test import TestCase
from django.contrib.auth import get_user_model
from nurse_admin.models import NurseAdmin
from hospital.models import Hospital


class NurseAdminModelTest(TestCase):
    def setUp(self):
        # Create a user instance with an email (required by your custom UserManager)
        self.user = get_user_model().objects.create_user(
            username="adminuser",
            email="adminuser@example.com",  # Provide the required email field
            password="password123",
        )

        # Create a hospital instance for the nurse admin
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            hospital_location="123 Test Street",  # Use the correct field name for the hospital model
        )

        # Create a NurseAdmin instance
        self.nurse_admin = NurseAdmin.objects.create(
            user=self.user,
            hospital_id=self.hospital,
            tel_no="+254712345678",
            location="Test Location",
            sub_location="Test Sub-location",
        )

    def test_nurse_admin_creation(self):
        # Test if the NurseAdmin instance was created successfully
        self.assertEqual(self.nurse_admin.user, self.user)
        self.assertEqual(self.nurse_admin.hospital_id, self.hospital)
        self.assertEqual(self.nurse_admin.tel_no, "+254712345678")
