from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('home/', views.seller_view, name='home'),  # Seller home page
    path('signup/', views.seller_signup_view, name='signup'),  # Seller signup
    path('logout/', views.seller_logout_view, name='logout'),  # Seller logout
    path('add/', views.seller_add_view, name='add'),  # Add seller's product
    path('delete/<int:id>/', views.delete_view, name='delete'),  # Delete seller's product
    path('edit/<int:pk>/', views.edit_view, name='edit'),  # Edit seller's product
]
