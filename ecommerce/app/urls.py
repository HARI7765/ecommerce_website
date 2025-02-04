from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('home/', views.home, name='home'),  # Added 'home' route for proper redirection
]
