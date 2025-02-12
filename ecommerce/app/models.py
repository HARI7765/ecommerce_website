# app/models.py
from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class MedicalEquipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='equipment/', null=True, blank=True)
    
    def __str__(self):
        return self.name