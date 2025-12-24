from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100) 
    isVendor = models.BooleanField(default=False)
    class Meta:
        db_table = "users"
