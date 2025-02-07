from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    description=models.CharField(max_length=500)
    dosage=models.IntegerField(max_length=200)

