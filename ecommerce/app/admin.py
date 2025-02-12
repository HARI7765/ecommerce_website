# app/admin.py
from django.contrib import admin
from .models import Medicine, MedicalEquipment

admin.site.register(Medicine)
admin.site.register(MedicalEquipment)