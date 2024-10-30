from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Mother
from hospital.models import Hospital
from next_of_kin.models import NextOfKin
from django.utils import timezone
from datetime import date

class MotherModelTest(TestCase):
    def setUp(self):
        """
        Set up a sample Mother instance for testing with related Hospital and NextOfKin instances.
        """
        # Create a hospital instance
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            hospital_location="123 Test Street"
        )

        # Create a NextOfKin instance
        self.kin = NextOfKin.objects.create(
            first_name="John",
            last_name="Doe",
            relationship="Brother",
            phone_number="987-654-3210"  # Correct field name
        )

        # Create a sample Mother instance
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1980, 5, 15),
            no_of_children=3,
            registered_date=timezone.now(),  
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="SubLocation1",
            village="Village1",
            hospital=self.hospital,
            kin=self.kin  
        )

    def test_mother_creation(self):
        """ Test if the Mother instance is created correctly. """
        self.assertEqual(self.mother.first_name, "Jane")
        self.assertEqual(self.mother.last_name, "Doe")
        self.assertEqual(self.mother.date_of_birth, date(1980, 5, 15))
        self.assertEqual(self.mother.no_of_children, 3)
        self.assertEqual(self.mother.tel_no, "123-456-7890")
        self.assertEqual(self.mother.marital_status, "Married")
        self.assertEqual(self.mother.sub_location, "SubLocation1")
        self.assertEqual(self.mother.village, "Village1")
        self.assertEqual(self.mother.hospital, self.hospital)
        self.assertEqual(self.mother.kin, self.kin)  

    def test_mother_str(self):
        """ Test the __str__ method of the Mother model. """
        self.assertEqual(str(self.mother), "Jane Doe")

    def test_field_max_length(self):
        """ Test the max_length constraint on CharFields. """
        mother = Mother(
            first_name="A" * 101,  
            last_name="B" * 101,  
            date_of_birth=date(1980, 5, 15),
            no_of_children=3,
            registered_date=timezone.now(),
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="C" * 101,  
            village="D" * 101,  
            hospital=self.hospital,
            kin=self.kin  
        )
        # full_clean will trigger validation checks for max_length
        with self.assertRaises(ValidationError):
            mother.full_clean()  

    def test_no_of_children_validation(self):
        """ Test that no_of_children field accepts only non-negative integers. """
        self.mother.no_of_children = -1
        with self.assertRaises(ValidationError):
            self.mother.full_clean()  # This should raise a ValidationError
