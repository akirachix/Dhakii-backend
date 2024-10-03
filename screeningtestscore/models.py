from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class ScreeningTestScore(models.Model):
    id = models.AutoField(primary_key=True)  # Unique ID for each test
    mother_id = models.ForeignKey("mother.Mother", on_delete=models.CASCADE)
    chp_id = models.ForeignKey("community_health_promoter.CHP", on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    total_score = models.PositiveSmallIntegerField()

    def __str__(self):
        return f" Total Score: {self.total_score}"

   
