from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from hospital.models import Hospital
from community_health_promoter.models import CHP


class Mother(models.Model):
    
    DUE_VISIT = 1
    VISITED = 0
    MISSED_VISIT = -1
    STATUS_CHOICES = [
        (DUE_VISIT, 'Due Visit'),
        (VISITED, 'Visited'),
        (MISSED_VISIT, 'Missed Visit'),
    ]
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    chp = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'user_role': 'chp'}, related_name='assigned_mothers' ) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_reg = models.DateField(default=timezone.now)   
    no_of_children = models.PositiveIntegerField()
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tel_no = models.CharField(max_length=15)
    marital_status = models.CharField(max_length=20)
    sub_location = models.CharField(max_length=255)
    village = models.CharField(max_length=255)

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=DUE_VISIT,
        help_text="1: Due Visit, 0: Visited, -1: Missed Visit"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if self.status not in [self.DUE_VISIT, self.VISITED, self.MISSED_VISIT]:
            raise ValidationError("Invalid status value.")

