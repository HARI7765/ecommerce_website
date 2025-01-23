
from django.contrib import admin
from .models import Medicine, MedicalEquipment
from .forms import MedicineForm, MedicalEquipmentForm

class MedicineAdmin(admin.ModelAdmin):
    form = MedicineForm

class MedicalEquipmentAdmin(admin.ModelAdmin):
    form = MedicalEquipmentForm

admin.site.register(Medicine, MedicineAdmin)
admin.site.register(MedicalEquipment, MedicalEquipmentAdmin)
