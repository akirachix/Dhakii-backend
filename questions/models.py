from django.core.exceptions import ValidationError
from django.db import models


class EPDSQuestion(models.Model):
    question = models.TextField(unique=True)  
    option_1 = models.TextField()
    first_score = models.IntegerField()
    option_2 = models.TextField()
    second_score = models.IntegerField()
    option_3 = models.TextField()
    third_score = models.IntegerField()
    option_4 = models.TextField()
    forth_score = models.IntegerField()

    def __str__(self):
        return self.question

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "option_1": self.option_1,
            "first_score": self.first_score,
            "option_2": self.option_2,
            "second_score": self.second_score,
            "option_3": self.option_3,
            "third_score": self.third_score,
            "option_4": self.option_4,
            "forth_score": self.forth_score,
        }

    def clean(self):
        # Ensure all score fields are within a valid range (0 to 3)
        for score in [
            self.first_score,
            self.second_score,
            self.third_score,
            self.forth_score,
        ]:
            if not (0 <= score <= 3):
                raise ValidationError(f"Score {score} is out of valid range (0-3)")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is done before saving
        super().save(*args, **kwargs)
