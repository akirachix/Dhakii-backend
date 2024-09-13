from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital
from django.conf import settings

class NurseAdmin(models.Model):
    """
    NurseAdmin Model - Stores information about nurse administrators.
    Fields:
        - admin_id: Primary key, unique for each nurse admin.
        - hospital_id: Foreign key to the Hospital model.
        - user_id: Foreign key to the User model.
        - location: Location of the nurse admin.
        - sub_location: Sub-location of the nurse admin.
        - created_at: Auto-set field for record creation timestamp.
        - updated_at: Auto-set field for record update timestamp.
    """
    admin_id = models.AutoField(primary_key=True)
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tel_no = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    sub_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Nurse Admin {self.user_id.username} ({self.hospital_id.name})"


