from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
    
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    restaurant_type = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    working_hours = models.CharField(max_length=25)
    restaurant_price = models.IntegerField()
    