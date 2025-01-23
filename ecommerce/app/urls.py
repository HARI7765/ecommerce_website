from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('cart/', views.cart, name='cart'),  # URL for viewing the cart
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # URL for adding an item to the cart
]
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This handles the root path
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),
]
