from django.test import TestCase
from django.contrib.auth import get_user_model
from nurse.models import Nurse
from hospital.models import Hospital
from django.core.exceptions import ValidationError


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
            hospital=self.hospital,
            gender="Female",
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )

    def test_nurse_creation(self):
        # Test if the Nurse instance was created successfully
        self.assertEqual(self.nurse.user, self.user)
        self.assertEqual(self.nurse.hospital, self.hospital)


class NurseModelUnhappyTest(TestCase):
    def setUp(self):
        # Create a user instance
        self.user = get_user_model().objects.create_user(
            username="nurseuser", email="nurseuser@example.com", password="password123"
        )

        # Create a hospital instance
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            hospital_location="123 Test Street",  # Use the correct field name for the hospital model
        )

    def test_missing_required_fields(self):
        """
        Test creating a Nurse instance with missing required fields should raise a ValidationError.
        """
        nurse = Nurse(
            user=self.user,
            hospital_id=self.hospital,
            gender="Female",  # reg_no and tel_no are missing
            sub_location="Test Sub-location",
        )
        with self.assertRaises(ValidationError):
            nurse.full_clean()  # This triggers model validation and should raise a ValidationError

    def test_invalid_gender(self):
        """
        Test creating a Nurse instance with an invalid gender should raise a ValidationError.
        """
        nurse = Nurse(
            user=self.user,
            hospital_id=self.hospital,
            gender="InvalidGender",  # Invalid gender
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )
        with self.assertRaises(ValidationError):
            nurse.full_clean()  # This triggers model validation and should raise a ValidationError

    def test_invalid_phone_number_format(self):
        """
        Test creating a Nurse instance with an invalid phone number should raise a ValidationError.
        """
        nurse = Nurse(
            user=self.user,
            hospital_id=self.hospital,
            gender="Female",
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )
    

    def test_missing_user(self):
        """
        Test creating a Nurse instance without a user should raise a ValidationError.
        """
        nurse = Nurse(
            user=None,  # Missing user
            hospital_id=self.hospital,
            gender="Female",
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )
        with self.assertRaises(ValidationError):
            nurse.full_clean()  # This triggers model validation and should raise a ValidationError

    def test_missing_hospital(self):
        """
        Test creating a Nurse instance without a hospital should raise a ValidationError.
        """
        nurse = Nurse(
            user=self.user,
            hospital_id=None,  # Missing hospital
            gender="Female",
            reg_no="RN123456",
            sub_location="Test Sub-location",
        )
        with self.assertRaises(ValidationError):
            nurse.full_clean()  # This triggers model validation and should raise a ValidationError
