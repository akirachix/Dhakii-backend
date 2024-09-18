from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital
from django.conf import settings
from django.core.validators import RegexValidator


class Nurse(models.Model):
    """
    Nurse Model - Stores information about nurses.
    """

    phone_number_validator = RegexValidator(
        regex=r"^\+?\d{10,15}$",
        message="Phone number must be between 10 and 15 digits and start with '+' if international.",
    )

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    nurse_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    tel_no = models.CharField(
        max_length=15, validators=[phone_number_validator]
    )  # Added phone number validator
    reg_no = models.CharField(max_length=50)
    sub_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Nurse {self.user.username} ({self.reg_no})"
