from django.test import TestCase
from django.contrib.auth import get_user_model  # For creating a valid user for CHP
from datetime import date
from screeningtestscore.models import ScreeningTestScore
from questions.models import EPDSQuestion
from mother.models import Mother  # Import the Mother model
from community_health_promoter.models import CHP  # Import the CHP model
from .models import Answer


class AnswerModelTest(TestCase):
    def setUp(self):
        # Create a valid User instance for CHP
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )

        # Create a valid CHP instance
        self.chp = CHP.objects.create(
            user=self.user,
            registered_date=date.today(),
            reg_no="CHP001",
            phone_number="0987654321",
            location="Test Location",
            sub_location="Test Sub-location",
            village="Test Village",
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

        # Create a valid EPDSQuestion instance
        self.question = EPDSQuestion.objects.create(
            question="How often have you been bothered by feeling down, depressed, or hopeless?",
            option_1="Never",
            first_score=0,
            option_2="Sometimes",
            second_score=1,
            option_3="Often",
            third_score=2,
            option_4="Always",
            forth_score=3,
        )

        # Provide the test_date, chp_id, and mother_id when creating ScreeningTestScore
        self.test_score = ScreeningTestScore.objects.create(
            total_score=0,
            test_date=date.today(),
            chp_id=self.chp,  # Assign the valid CHP instance
            mother_id=self.mother,  # Assign the valid Mother instance
        )

    def test_create_answer(self):
        answer = Answer.objects.create(
            question=self.question, test=self.test_score, score=3
        )

        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.test, self.test_score)
        self.assertEqual(answer.score, 3)

    def test_answer_str(self):
        answer = Answer.objects.create(
            question=self.question, test=self.test_score, score=4
        )
        expected_str = f"Answer for Question {self.question.id} - Score: {answer.score}"
        self.assertEqual(str(answer), expected_str)
