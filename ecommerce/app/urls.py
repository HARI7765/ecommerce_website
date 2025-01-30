from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Signup page
    path('signup/', views.signup, name='signup'),

    # Signin page
    path('signin/', views.signin, name='signin'),

    # Cart page
    path('cart/', views.cart, name='cart'),

    # Add to cart (with product ID)
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Add medicine (admin-only)
    path('add_medicine/', views.add_medicine, name='add_medicine'),

    # Add medical equipment (admin-only)
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),

    # Admin page
    path('admin_page/', views.admin_page, name='admin_page'),
]