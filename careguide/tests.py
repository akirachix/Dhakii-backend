from django.test import TestCase
from careguide.models import Careguide
from django.core.exceptions import ValidationError


class CareguideModelTest(TestCase):
    
    def setUp(self):
        # Create a Careguide instance for testing
        self.careguide = Careguide.objects.create(
            category="Mental Health",
            title="Postpartum Care",
            image="http://example.com/image.jpg",
            subtitle="A guide for postpartum care",
            content="<h1>Postpartum Care</h1><p>Content here</p>",
            author="Dr. Jane Doe"
        )

    def test_careguide_creation(self):
        # Test if the Careguide instance was created successfully
        self.assertEqual(self.careguide.category, "Mental Health")
        self.assertEqual(self.careguide.title, "Postpartum Care")
        self.assertEqual(self.careguide.image, "http://example.com/image.jpg")
        self.assertEqual(self.careguide.subtitle, "A guide for postpartum care")
        self.assertEqual(self.careguide.author, "Dr. Jane Doe")

    def test_careguide_str(self):
        # Test the __str__ method of the Careguide model
        self.assertEqual(str(self.careguide), "Postpartum Care")


class CareguideModelUnhappyTest(TestCase):

    def test_missing_title(self):
        """
        Test creating a Careguide instance with a missing title should raise a ValidationError.
        """
        careguide = Careguide(
            category="Mental Health",
            image="http://example.com/image.jpg",
            subtitle="A guide for postpartum care",
            content="<h1>Postpartum Care</h1><p>Content here</p>",
            author="Dr. Jane Doe"
        )
        with self.assertRaises(ValidationError):
            careguide.full_clean()  

    def test_invalid_image_url(self):
        """
        Test creating a Careguide instance with an invalid URL for the image should raise a ValidationError.
        """
        careguide = Careguide(
            category="Mental Health",
            title="Postpartum Care",
            image="invalid_url",  # Invalid URL format
            subtitle="A guide for postpartum care",
            content="<h1>Postpartum Care</h1><p>Content here</p>",
            author="Dr. Jane Doe"
        )
        with self.assertRaises(ValidationError):
            careguide.full_clean()  

    def test_missing_category(self):
        """
        Test creating a Careguide instance with a missing category should raise a ValidationError.
        """
        careguide = Careguide(
            category="",
            title="Postpartum Care",
            image="http://example.com/image.jpg",
            subtitle="A guide for postpartum care",
            content="<h1>Postpartum Care</h1><p>Content here</p>",
            author="Dr. Jane Doe"
        )
        with self.assertRaises(ValidationError):
            careguide.full_clean() 

    def test_missing_content(self):
        """
        Test creating a Careguide instance with missing content should raise a ValidationError.
        """
        careguide = Careguide(
            category="Mental Health",
            title="Postpartum Care",
            image="http://example.com/image.jpg",
            subtitle="A guide for postpartum care",
            content="",  # Missing content
            author="Dr. Jane Doe"
        )
        with self.assertRaises(ValidationError):
            careguide.full_clean()  

    def test_missing_author(self):
        """
        Test creating a Careguide instance without an author (optional field).
        Since the author field is optional, this should pass.
        """
        careguide = Careguide(
            category="Mental Health",
            title="Postpartum Care",
            image="http://example.com/image.jpg",
            subtitle="A guide for postpartum care",
            content="<h1>Postpartum Care</h1><p>Content here</p>"
            # No author provided
        )
        try:
            careguide.full_clean()  # Should pass without raising an error
        except ValidationError:
            self.fail("Careguide.full_clean() raised ValidationError unexpectedly!")

