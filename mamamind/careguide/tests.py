from django.core.exceptions import ValidationError
from django.test import TestCase
from careguide.models import Careguide

class CareguideModelTest(TestCase):

    def test_careguide_creation(self):
        """
        Happy path: Test if the Careguide object is created successfully with valid data.
        """
        careguide = Careguide.objects.create(
            title="Sample Title",
            content="Sample content for Careguide.",
            author="Author"
        )
        self.assertEqual(careguide.title, "Sample Title")
        self.assertEqual(careguide.content, "Sample content for Careguide.")
        self.assertEqual(careguide.author, "Author")

    def test_careguide_blank_author(self):
        """
        Happy path: Test if a Careguide object can be created with a blank author field.
        """
        careguide = Careguide.objects.create(
            title="Sample Title",
            content="Sample content for Careguide.",
            author=""  
        )
        self.assertEqual(careguide.title, "Sample Title")
        self.assertEqual(careguide.content, "Sample content for Careguide.")
        self.assertEqual(careguide.author, "")

    def test_careguide_creation_without_title(self):
        """
        Unhappy path: Test if a Careguide object raises a ValidationError when created without a title.
        """
        careguide = Careguide(
            title="",  
            content="Content",
            author="Author"
        )
        with self.assertRaises(ValidationError) as cm:
            careguide.full_clean() 
        self.assertIn('Title cannot be empty.', str(cm.exception))

    def test_careguide_title_max_length(self):
        """
        Unhappy path: Test if Careguide object raises a ValidationError for exceeding title max length.
        """
        careguide = Careguide(
            title="A" * 256,  
            content="Content",
            author="Author"
        )
        with self.assertRaises(ValidationError) as cm:
            careguide.full_clean()  
        self.assertIn('Ensure this value has at most 255 characters (it has 256).', str(cm.exception))

    def test_careguide_creation_without_content(self):
        """
        Unhappy path: Test if a Careguide object can be created with empty content.
        """
        careguide = Careguide.objects.create(
            title="Sample Title",
            content="",  
            author="Author"
        )
        self.assertEqual(careguide.content, "")
