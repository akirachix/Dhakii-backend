from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings  # To refer to the User model


class CHP(models.Model):
    phone_number_validator = RegexValidator(
        regex=r"^\d{10}$", message="Phone number must be exactly 10 digits."
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Ensure valid ForeignKey to User
    registered_date = models.DateField()
    reg_no = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, validators=[phone_number_validator])
    location = models.TextField()
    sub_location = models.CharField(max_length=255)
    village = models.CharField(max_length=255)

    def __str__(self):
        # Use the username or another field of the user
        return f"{self.reg_no} - {self.user.username}"  # Reference the username of the related user