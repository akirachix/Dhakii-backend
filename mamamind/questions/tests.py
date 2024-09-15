from django.test import TestCase
from django.contrib.auth import get_user_model
from mother.models import Mother
from community_health_promoter.models import CHP
from screeningtestscore.models import ScreeningTestScore
from datetime import date


class ScreeningTestScoreModelTest(TestCase):
    def setUp(self):
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Create a valid Mother instance
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth="1990-01-01",
            no_of_children=2,
            date_of_reg=date.today(),
            tel_no="1234567890",
            marital_status="Married",
            sub_location="Test Sub-location",
            village="Test Village",
        )

        # Create a valid CHP instance, providing a user
        self.chp = CHP.objects.create(
            user=self.user,  # Pass the created user here
            registered_date=date.today(),
            reg_no="CHP001",
            phone_number="0987654321",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
        )

        # Create a ScreeningTestScore instance with valid mother and chp
        self.screening_test = ScreeningTestScore.objects.create(
            mother_id=self.mother,
            chp_id=self.chp,
            test_date=date.today(),
            total_score=15,
        )

    def test_create_screening_test_score(self):
        # Test that the ScreeningTestScore instance was created correctly
        self.assertEqual(self.screening_test.mother_id, self.mother)
        self.assertEqual(self.screening_test.chp_id, self.chp)
        self.assertEqual(self.screening_test.total_score, 15)
        self.assertEqual(self.screening_test.test_date, date.today())

    def test_screening_test_score_str(self):
        # Test the string representation of the ScreeningTestScore
        expected_str = f"Test {self.screening_test.test_id} - Total Score: 15"
        self.assertEqual(str(self.screening_test), expected_str)

    def test_total_score_positive(self):
        # Ensure total score is a positive integer
        self.assertGreaterEqual(self.screening_test.total_score, 0)

    def test_screening_test_score_relationships(self):
        # Ensure relationships with Mother and CHP models work correctly
        self.assertEqual(self.screening_test.mother_id.first_name, "Jane")
        self.assertEqual(self.screening_test.chp_id.reg_no, "CHP001")
