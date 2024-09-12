from django.db import models
from questions.models import EPDSQuestion
from screeningtestscore.models import ScreeningTestScore

class Answer(models.Model):
    question = models.ForeignKey(EPDSQuestion, on_delete=models.CASCADE)
    test = models.ForeignKey(ScreeningTestScore, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"Answer for Question {self.question.id} - Score: {self.score}"










# from django.db import models


# class Answer(models.Model):
#     question = models.ForeignKey('questions.EPDSQuestion', on_delete=models.CASCADE)  
#     test = models.ForeignKey('screeningtestscore.ScreeningTestScore', on_delete=models.CASCADE) 
#     score = models.IntegerField()

#     def __str__(self):
#         return f"Answer for Question {self.question.id} - Score: {self.score}"


