from django.db import models

class ScreeningTestScore(models.Model):
    test_id = models.AutoField(primary_key=True)  # Unique ID for each test
    # mother_id = models.ForeignKey('Mother', on_delete=models.CASCADE)  
    # chp_id = models.ForeignKey('CHP', on_delete=models.CASCADE)  
    test_date = models.DateField()  
    total_score = models.PositiveSmallIntegerField()  

    def __str__(self):
        return f"Test {self.test_id} - Total Score: {self.total_score}"



