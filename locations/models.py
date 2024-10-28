from django.db import models

class Location(models.Model):
    location = models.CharField(max_length=255) 
    sub_location = models.CharField(max_length=255, blank=True, null=True)   
    village = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('location', 'sub_location', 'village') 
    def __str__(self):
        parts = [self.location]
        if self.sub_location:
            parts.append(self.sub_location)
        if self.village:
            parts.append(self.village)
        return " > ".join(parts) 