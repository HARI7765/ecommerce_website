from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    proof = models.FileField(upload_to='proofs/')

    def __str__(self):
        return self.user.username


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='medicines/')

    def __str__(self):
        return self.name


class MedicalEquipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='equipment/')

    def __str__(self):
        return self.name
from django import forms
from .models import Medicine, MedicalEquipment

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class MedicalEquipmentForm(forms.ModelForm):
    class Meta:
        model = MedicalEquipment
        fields = '__all__'