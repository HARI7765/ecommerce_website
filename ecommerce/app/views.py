from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Medicine, MedicalEquipment  # Make sure MedicalEquipment model exists
from .forms import MedicineForm, MedicalEquipmentForm
from django.contrib.auth.models import User


#seller side
