from django.db import models

class CHP(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)  
    registered_date = models.DateField()
    reg_no = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    sub_location = models.CharField(max_length=255)  
    village = models.CharField(max_length=255) 


    def __str__(self):
        return f"{self.reg_no} {self.user_id}"



# id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True, null=True)
#     last_name = models.CharField(max_length=150, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(default=datetime.now)
#     updated_at = models.DateTimeField(default=datetime.now)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)