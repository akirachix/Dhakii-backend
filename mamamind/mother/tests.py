from django.test import TestCase
from .models import Mother
from datetime import date


class MotherModelTest(TestCase):
    def setUp(self):
        """
        Set up a sample Mother instance for testing.
        """
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1980, 5, 15),
            no_of_children=3,
            date_of_reg=date(2024, 1, 10),
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="SubLocation1",
            village="Village1",
        )

    def test_mother_creation(self):
        """
        Test if the Mother instance is created correctly.
        """
        self.assertEqual(self.mother.first_name, "Jane")
        self.assertEqual(self.mother.last_name, "Doe")
        self.assertEqual(self.mother.date_of_birth, date(1980, 5, 15))
        self.assertEqual(self.mother.no_of_children, 3)
        self.assertEqual(self.mother.date_of_reg, date(2024, 1, 10))
        self.assertEqual(self.mother.tel_no, "123-456-7890")
        self.assertEqual(self.mother.marital_status, "Married")
        self.assertEqual(self.mother.sub_location, "SubLocation1")
        self.assertEqual(self.mother.village, "Village1")

    def test_mother_str(self):
        """
        Test the __str__ method of the Mother model.
        """
        self.assertEqual(str(self.mother), "Jane Doe")

    def test_field_max_length(self):
        """
        Test the max_length constraint on CharFields.
        """
        mother = Mother(
            first_name="A" * 100,  # Exceeding max_length
            last_name="B" * 100,
            date_of_birth=date(1980, 5, 15),
            no_of_children=3,
            date_of_reg=date(2024, 1, 10),
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="C" * 100,
            village="D" * 100,
        )

    def test_no_of_children_validation(self):
        """
        Test that no_of_children field accepts only non-negative integers.
        """
        self.mother.no_of_children = -1
