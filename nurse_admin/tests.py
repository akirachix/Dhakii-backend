from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from nurse_admin.models import NurseAdmin
from hospital.models import Hospital


class NurseAdminModelTest(TestCase):
    def setUp(self):
        # Create a user instance with an email
        self.user = get_user_model().objects.create_user(
            username="adminuser",
            email="adminuser@example.com",
            password="password123",
        )

        # Create a hospital instance for the nurse admin
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            hospital_location="123 Test Street",
        )

        # Create a valid NurseAdmin instance
        self.nurse_admin = NurseAdmin.objects.create(
            user=self.user,
            hospital_id=self.hospital,
            tel_no="+254712345678",
            location="Test Location",
            sub_location="Test Sub-location",
        )

    def test_nurse_admin_creation(self):
        # Test if the NurseAdmin instance was created successfully (happy path)
        self.assertEqual(self.nurse_admin.user, self.user)
        self.assertEqual(self.nurse_admin.hospital_id, self.hospital)
        self.assertEqual(self.nurse_admin.tel_no, "+254712345678")

    def test_missing_required_fields(self):
        """
        Test creating a NurseAdmin instance with missing required fields should raise a ValidationError.
        """
        nurse_admin = NurseAdmin(
            user=self.user,
            hospital_id=self.hospital,
            location="Test Location",
            sub_location="Test Sub-location",
        )
        # `tel_no` is missing, so validation should fail
        with self.assertRaises(ValidationError):
            nurse_admin.full_clean()  # This triggers model validation

    def test_invalid_phone_number_format(self):
        """
        Test creating a NurseAdmin instance with an invalid phone number should raise a ValidationError.
        """
        nurse_admin = NurseAdmin(
            user=self.user,
            hospital_id=self.hospital,
            tel_no="invalid_phone",  # Invalid phone number format
            location="Test Location",
            sub_location="Test Sub-location",
        )
        # Phone number is invalid, so validation should fail
        with self.assertRaises(ValidationError):
            nurse_admin.full_clean()  # This triggers model validation

    def test_missing_user(self):
        """
        Test creating a NurseAdmin instance without a user should raise a ValidationError.
        """
        nurse_admin = NurseAdmin(
            user=None,  # Missing user
            hospital_id=self.hospital,
            tel_no="+254712345678",
            location="Test Location",
            sub_location="Test Sub-location",
        )
        # User is missing, so validation should fail
        with self.assertRaises(ValidationError):
            nurse_admin.full_clean()  # This triggers model validation

    def test_missing_hospital(self):
        """
        Test creating a NurseAdmin instance without a hospital should raise a ValidationError.
        """
        nurse_admin = NurseAdmin(
            user=self.user,
            hospital_id=None,  # Missing hospital
            tel_no="+254712345678",
            location="Test Location",
            sub_location="Test Sub-location",
        )
        # Hospital is missing, so validation should fail
        with self.assertRaises(ValidationError):
            nurse_admin.full_clean()  # This triggers model validation
