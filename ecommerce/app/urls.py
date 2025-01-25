# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('signin/', views.signin, name='signin'),  # Signin page
    path('cart/', views.cart, name='cart'),  # Cart page
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('add_medicine/', views.add_medicine, name='add_medicine'),  # Add medicine
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),  # Add equipment
    path('admin_page/', views.admin_page, name='admin_page'),  # Admin page
]
