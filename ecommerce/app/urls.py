from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('cart/', views.cart, name='cart'),  # URL for viewing the cart
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # URL for adding an item to the cart
]
