from django.test import TestCase
from questions.models import EPDSQuestion
from screeningtestscore.models import ScreeningTestScore
from answers.models import Answer
from django.core.exceptions import ValidationError
from datetime import date
from mother.models import Mother
from community_health_promoter.models import CHP
from django.contrib.auth import get_user_model
class AnswerModelTest(TestCase):
    def setUp(self):
        """
        Set up EPDSQuestion and ScreeningTestScore instances for the Answer model.
        """
        # Create a valid User instance for CHP
        self.user = get_user_model().objects.create_user(
            username="chpuser", email="chpuser@example.com", password="password123"
        )
        # Create Mother instance
        self.mother = Mother.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth="1980-05-15",
            no_of_children=2,
            date_of_reg="2023-01-01",
            tel_no="123-456-7890",
            marital_status="Married",
            sub_location="SubLocation1",
            village="Village1",
        )
        # Create CHP instance
        self.chp = CHP.objects.create(
            user=self.user,
            registered_date="2023-01-01",
            reg_no="CHP123",
            location="Location1",
            sub_location="SubLocation1",
            village="Village1",
        )
        # Create a ScreeningTestScore instance
        self.test_score = ScreeningTestScore.objects.create(
            mother=self.mother, chp=self.chp, test_date=date.today(), total_score=15
        )
        # Create an EPDSQuestion instance using the correct field name
        self.question = EPDSQuestion.objects.create(
            question="How often have you felt sad?",  # Correct field name
            option_1="Not at all",
            first_score=0,
            option_2="Some of the time",
            second_score=1,
            option_3="A lot of the time",
            third_score=2,
            option_4="Nearly all the time",
            forth_score=3,
        )
def test_answer_creation(self):
    """
    Happy path: Test if the Answer instance is created successfully.
    """
    answer = Answer.objects.create(
        question=self.question, test=self.test_score, score=2
    )
    self.assertEqual(answer.question, self.question)
    self.assertEqual(answer.test, self.test_score)
    self.assertEqual(answer.score, 2)
    self.assertEqual(
        str(answer), f"Answer for Question {self.question.id} - Score: {answer.score}"
    )
    def test_missing_question(self):
        """
        Unhappy path: Test that missing question raises a ValidationError.
        """
        answer = Answer(
            question=None, test=self.test_score, score=2  # Missing question
        )
        with self.assertRaises(ValidationError):
            answer.full_clean()  # This should raise a ValidationError
    def test_missing_test(self):
        """
        Unhappy path: Test that missing test raises a ValidationError.
        """
        answer = Answer(question=self.question, test=None, score=2)  # Missing test
        with self.assertRaises(ValidationError):
            answer.full_clean()  # This should raise a ValidationError
    def test_missing_score(self):
        """
        Unhappy path: Test that missing score raises a ValidationError.
        """
        answer = Answer(
            question=self.question, test=self.test_score, score=None  # Missing score
        )
        with self.assertRaises(ValidationError):
            answer.full_clean()  # This should raise a ValidationError
    def test_negative_score(self):
        """
        Unhappy path: Test that a negative score raises a ValidationError.
        """
        answer = Answer(
            question=self.question,
            test=self.test_score,
            score=-1,  # Invalid negative score
        )
        with self.assertRaises(ValidationError):
            answer.full_clean()  # This should raise a ValidationError