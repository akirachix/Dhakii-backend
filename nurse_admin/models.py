from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from hospital.models import Hospital


class NurseAdmin(models.Model):
    """
    NurseAdmin Model - Stores information about nurse administrators.
    """
    id = models.AutoField(primary_key=True)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    sub_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Nurse Admin {self.user.username} ({self.hospital_id.name})"
