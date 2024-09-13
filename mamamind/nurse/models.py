from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital
from django.conf import settings



class Nurse(models.Model):
    """
    Nurse Model - Stores information about nurses.
    Fields:
        - nurse_id: AutoField, primary key.
        - user_id: Foreign key to the User model.
        - gender: Gender of the nurse.
        - reg_no: Registration number of the nurse.
        - tel_no: Telephone number.
        - bio: Brief biography of the nurse.
        - sub_location: Location (sub-location) of the nurse.
        - picture: Image field for the nurse's profile picture.
    """
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    nurse_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    tel_no = models.CharField(max_length=15)
    reg_no = models.CharField(max_length=50)
    sub_location = models.CharField(max_length=255)   

    def __str__(self):
        return f"Nurse {self.user_id.username} ({self.reg_no})"

    

