from django.db import models
from questions.models import EPDSQuestion
from screeningtestscore.models import ScreeningTestScore
from django.core.exceptions import ValidationError  # Import ValidationError

class Answer(models.Model):
    question = models.ForeignKey(EPDSQuestion, on_delete=models.CASCADE)
    test = models.ForeignKey(ScreeningTestScore, on_delete=models.CASCADE)
    score = models.IntegerField()
    def __str__(self):
        return f"Answer for Question {self.question.id} - Score: {self.score}"
    def clean(self):
        # Ensure the score is not negative
        if self.score is not None and self.score < 0:
            raise ValidationError("Score cannot be negative.")
    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation before saving
        self.full_clean()
        super().save(*args, **kwargs)