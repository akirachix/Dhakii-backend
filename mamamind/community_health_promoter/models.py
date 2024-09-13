from django.db import models
from django.conf import settings

class CHP(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    registered_date = models.DateField()
    reg_no = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    sub_location = models.CharField(max_length=255)  
    village = models.CharField(max_length=255) 


    def __str__(self):
        return f"{self.reg_no} {self.user_id}"



