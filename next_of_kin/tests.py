from django.test import TestCase
from django.utils import timezone
from .models import NextOfKin
from django.core.exceptions import ValidationError

class NextOfKinModelTest(TestCase):
    def setUp(self):
        """
        Set up a sample NextOfKin instance for testing.
        """
        # Create a NextOfKin instance
        self.next_of_kin = NextOfKin.objects.create(
            first_name="John",
            last_name="Doe",
            relationship="Brother",
            phone_number="987-654-3210",  # Correct field name
        )

    def test_next_of_kin_creation(self):
        """ Test if the NextOfKin instance is created correctly. """
        self.assertEqual(self.next_of_kin.first_name, "John")
        self.assertEqual(self.next_of_kin.last_name, "Doe")
        self.assertEqual(self.next_of_kin.relationship, "Brother")
        self.assertEqual(self.next_of_kin.phone_number, "987-654-3210")
        self.assertTrue(self.next_of_kin.created_at)
        self.assertTrue(self.next_of_kin.updated_at)
        self.assertTrue(self.next_of_kin.created_at <= timezone.now())
        self.assertTrue(self.next_of_kin.updated_at <= timezone.now())

    def test_next_of_kin_str(self):
        """ Test the __str__ method of the NextOfKin model. """
        self.assertEqual(str(self.next_of_kin), "John Doe - Brother")

    def test_phone_number_max_length(self):
        """ Test the max_length constraint on the phone_number field. """
        next_of_kin = NextOfKin(
            first_name="Jane",
            last_name="Smith",
            relationship="Sister",
            phone_number="1" * 15,  # Max length
        )
        try:
            next_of_kin.full_clean()  # This should pass validation
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_relationship_max_length(self):
        """ Test the max_length constraint on the relationship field. """
        next_of_kin = NextOfKin(
            first_name="Jane",
            last_name="Smith",
            relationship="A" * 50,  # Max length
            phone_number="123-456-7890",
        )
        try:
            next_of_kin.full_clean()  # This should pass validation
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")


class NextOfKinModelUnhappyPathTest(TestCase):
    def test_missing_first_name(self):
        """ Unhappy path: Test if missing first_name raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name=None,  # Missing first name
            last_name="Doe",
            relationship="Brother",
            phone_number="987-654-3210",
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError

    def test_missing_last_name(self):
        """ Unhappy path: Test if missing last_name raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name="John",
            last_name=None,  # Missing last name
            relationship="Brother",
            phone_number="987-654-3210",
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError

    def test_missing_relationship(self):
        """ Unhappy path: Test if missing relationship raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name="John",
            last_name="Doe",
            relationship=None,  # Missing relationship
            phone_number="987-654-3210",
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError

    def test_phone_number_exceeds_max_length(self):
        """ Unhappy path: Test if phone_number exceeds max_length and raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name="John",
            last_name="Doe",
            relationship="Brother",
            phone_number="1" * 16,  # Exceeding max_length of 15
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError

    def test_relationship_exceeds_max_length(self):
        """ Unhappy path: Test if relationship exceeds max_length and raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name="John",
            last_name="Doe",
            relationship="A" * 51,  # Exceeding max_length of 50
            phone_number="987-654-3210",
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError

    def test_invalid_phone_number(self):
        """ Unhappy path: Test if an invalid phone number format raises a ValidationError. """
        next_of_kin = NextOfKin(
            first_name="John",
            last_name="Doe",
            relationship="Brother",
            phone_number="invalid-phone-number",  # Invalid phone number format
        )
        with self.assertRaises(ValidationError):
            next_of_kin.full_clean()  # This should raise a ValidationError
