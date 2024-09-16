from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import EPDSQuestion


class EPDSQuestionModelTest(TestCase):
    def test_create_epds_question_with_missing_question(self):
        # Test creating a question with a missing question text
        question = EPDSQuestion(
            option_1="Never",
            first_score=0,
            option_2="Sometimes",
            second_score=1,
            option_3="Often",
            third_score=2,
            option_4="Always",
            forth_score=3,
        )
        with self.assertRaises(ValidationError):
            question.full_clean()  # This will trigger the validation

    def test_create_epds_question_with_invalid_scores(self):
        # Test creating a question with an invalid score
        question = EPDSQuestion(
            question="How often have you been bothered by feeling down, depressed, or hopeless?",
            option_1="Never",
            first_score=-1,  # Invalid score
            option_2="Sometimes",
            second_score=1,
            option_3="Often",
            third_score=2,
            option_4="Always",
            forth_score=3,
        )
        with self.assertRaises(ValidationError):
            question.full_clean()  # This will trigger the validation

    def test_create_epds_question_with_duplicate_question(self):
        # Create the first question
        EPDSQuestion.objects.create(
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
        # Attempt to create a duplicate question
        with self.assertRaises(IntegrityError):
            EPDSQuestion.objects.create(
                question="How often have you been bothered by feeling down, depressed, or hopeless?",  # Duplicate
                option_1="Never",
                first_score=0,
                option_2="Sometimes",
                second_score=1,
                option_3="Often",
                third_score=2,
                option_4="Always",
                forth_score=3,
            )


class EPDSQuestionModelTest(TestCase):
    def test_create_valid_epds_question(self):
        # Test creating a valid EPDSQuestion instance
        question = EPDSQuestion(
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
        try:
            question.full_clean()  # This will validate the instance
            question.save()  # Save to the database
        except ValidationError:
            self.fail("EPDSQuestion instance raised ValidationError unexpectedly!")

        # Verify the instance was saved correctly
        saved_question = EPDSQuestion.objects.get(
            question="How often have you been bothered by feeling down, depressed, or hopeless?"
        )
        self.assertEqual(saved_question.option_1, "Never")
        self.assertEqual(saved_question.first_score, 0)
        self.assertEqual(saved_question.option_2, "Sometimes")
        self.assertEqual(saved_question.second_score, 1)
        self.assertEqual(saved_question.option_3, "Often")
        self.assertEqual(saved_question.third_score, 2)
        self.assertEqual(saved_question.option_4, "Always")
        self.assertEqual(saved_question.forth_score, 3)
