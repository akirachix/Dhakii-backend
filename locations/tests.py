from django.core.exceptions import ValidationError
from django.test import TestCase
from locations.models import Location


class LocationModelTest(TestCase):

    def setUp(self):
        # Create a valid Location instance for happy path testing
        self.location = Location.objects.create(
            location="Nairobi",
            sub_location="Kibera",
            village="Makina"
        )

    def test_location_creation(self):
        """
        Test if the Location instance was created successfully (happy path).
        """
        self.assertEqual(self.location.location, "Nairobi")
        self.assertEqual(self.location.sub_location, "Kibera")
        self.assertEqual(self.location.village, "Makina")

    def test_missing_location(self):
        """
        Test creating a Location instance without 'location' should raise a ValidationError.
        """
        location = Location(
            location=None,  # Missing location
            sub_location="Kibera",
            village="Makina"
        )
        # 'location' is required, so validation should fail
        with self.assertRaises(ValidationError):
            location.full_clean()  

    def test_missing_sub_location(self):
        """
        Test creating a Location instance without 'sub_location' should pass since it's optional.
        """
        location = Location(
            location="Nairobi",
            sub_location=None,  # sub_location is optional
            village="Makina"
        )
        # This should pass as 'sub_location' is not required
        try:
            location.full_clean() 
            location.save()
        except ValidationError:
            self.fail("Location creation failed unexpectedly when 'sub_location' is missing.")

    def test_missing_village(self):
        """
        Test creating a Location instance without 'village' should pass since it's optional.
        """
        location = Location(
            location="Nairobi",
            sub_location="Kibera",
            village=None  # village is optional
        )
        # This should pass as 'village' is not required
        try:
            location.full_clean()  
            location.save()
        except ValidationError:
            self.fail("Location creation failed unexpectedly when 'village' is missing.")

    def test_duplicate_location_combination(self):
        """
        Test creating a Location instance with a duplicate combination of location, sub_location, and village.
        """
        duplicate_location = Location(
            location="Nairobi",
            sub_location="Kibera",
            village="Makina"
        )
        # Duplicate combination should raise an IntegrityError (due to unique_together constraint)
        with self.assertRaises(ValidationError):
            duplicate_location.full_clean()  # This triggers model validation

    def test_blank_location(self):
        """
        Test creating a Location instance with an empty 'location' should raise a ValidationError.
        """
        location = Location(
            location="",  # Blank location
            sub_location="Kibera",
            village="Makina"
        )
        # Blank 'location' should fail validation
        with self.assertRaises(ValidationError):
            location.full_clean()  

    def test_long_location_name(self):
        """
        Test creating a Location instance with a 'location' name exceeding max length should raise a ValidationError.
        """
        long_location = "Nairobi" * 50  # Exceeding 255 characters
        location = Location(
            location=long_location,
            sub_location="Kibera",
            village="Makina"
        )
        # Location name exceeding max_length should fail validation
        with self.assertRaises(ValidationError):
            location.full_clean()  
