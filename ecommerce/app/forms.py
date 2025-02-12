# app/forms.py
from django import forms
from .models import Medicine, MedicalEquipment

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'price', 'image']

class MedicalEquipmentForm(forms.ModelForm):
    class Meta:
        model = MedicalEquipment
        fields = ['name', 'description', 'price', 'image']