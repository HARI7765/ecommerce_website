from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('home/', views.seller_view, name='home'),
    path('signup/', views.seller_signup_view, name='signup'),
    path('logout/', views.seller_logout_view, name='logout'),
    path('add/', views.seller_add_view, name='add'),
    path('delete/<int:id>/', views.delete_view, name='delete'),
    path('edit/<int:pk>/', views.edit_view, name='edit'),
]
