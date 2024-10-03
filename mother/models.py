from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone


class Mother(models.Model):
    # Defining constants for better readability
    DUE_VISIT = 1
    VISITED = 0
    MISSED_VISIT = -1
    STATUS_CHOICES = [
        (DUE_VISIT, 'Due Visit'),
        (VISITED, 'Visited'),
        (MISSED_VISIT, 'Missed Visit'),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_reg = models.DateField(default=timezone.now)   
    no_of_children = models.PositiveIntegerField()
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tel_no = models.CharField(max_length=15)
    marital_status = models.CharField(max_length=20)
    sub_location = models.CharField(max_length=100)
    
    village = models.CharField(max_length=100)
    # Adding the numeric status field
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=DUE_VISIT,
        help_text="1: Due Visit, 0: Visited, -1: Missed Visit"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        # Ensure status is one of the allowed values (1, 0, -1)
        if self.status not in [self.DUE_VISIT, self.VISITED, self.MISSED_VISIT]:
            raise ValidationError("Invalid status value.")

