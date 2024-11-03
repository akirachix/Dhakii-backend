from django.test import TestCase
from django.contrib.auth import get_user_model
from mother.models import Mother
from community_health_promoter.models import CHP
from screeningtestscore.models import ScreeningTestScore
from datetime import date
from django.core.exceptions import ValidationError


class ScreeningTestScoreModelTest(TestCase):
    def setUp(self):
        """
        Set up the User, Mother, and CHP instances for the ScreeningTestScore model.
        """
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Create Mother instance
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth="1980-05-15",
            no_of_children=2,
            registered_date="2023-01-01",
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="SubLocation1",
            village="Village1",
        )

        # Create CHP instance without 'registered_date'
        self.chp = CHP.objects.create(
            user=self.user,
            reg_no="CHP123",
            location="Location1",
            sub_location="SubLocation1",
            village="Village1",
        )

    def test_screening_test_score_creation(self):
        """
        Happy path: Test if the ScreeningTestScore instance is created successfully.
        """
        screening_test = ScreeningTestScore.objects.create(
            mother_id=self.mother, chp_id=self.chp, test_date=date.today(), total_score=10
        )

        self.assertEqual(screening_test.mother_id, self.mother)
        self.assertEqual(screening_test.chp_id, self.chp)
        self.assertEqual(screening_test.total_score, 10)
        self.assertIsInstance(screening_test.test_date, date)


class ScreeningTestScoreModelUnhappyPathTest(TestCase):
    def setUp(self):
        """
        Set up the User, Mother, and CHP instances for the ScreeningTestScore model.
        """
        # Create a valid User instance
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Create Mother instance
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth="1980-05-15",
            no_of_children=2,
            registered_date="2023-01-01",
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="SubLocation1",
            village="Village1",
        )

        # Create CHP instance without 'registered_date'
        self.chp = CHP.objects.create(
            user=self.user,
            reg_no="CHP123",
            location="Location1",
            sub_location="SubLocation1",
            village="Village1",
        )

    def test_negative_total_score(self):
        """
        Unhappy path: Test that a negative total_score raises a ValidationError.
        """
        screening_test = ScreeningTestScore(
            mother_id=self.mother,
            chp_id=self.chp,
            test_date=date.today(),
            total_score=-5,  # Invalid negative score
        )
        with self.assertRaises(ValidationError):
            screening_test.full_clean()  # This should raise a ValidationError
