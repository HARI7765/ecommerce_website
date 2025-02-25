from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Medicine, MedicalEquipment

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_login(self):
        response = self.client.post(reverse('app:signin'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_user_signup(self):
        response = self.client.post(reverse('app:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful signup

class MedicineTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='adminpass')
        self.client.login(username='admin', password='adminpass')

    def test_add_medicine(self):
        response = self.client.post(reverse('app:add_medicine'), {
            'name': 'Test Medicine',
            'description': 'Test Description',
            'price': 10.99
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after adding
        self.assertEqual(Medicine.objects.count(), 1)

class MedicalEquipmentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='adminpass')
        self.client.login(username='admin', password='adminpass')

    def test_add_medical_equipment(self):
        response = self.client.post(reverse('app:add_medical_equipment'), {
            'name': 'Test Equipment',
            'description': 'Test Description',
            'price': 100.99
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after adding
        self.assertEqual(MedicalEquipment.objects.count(), 1)
