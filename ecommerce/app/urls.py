from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Admin/Product Management URLs
    path('admin_page/', views.admin_page, name='admin_page'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),

    # Seller URLs
    path('seller/home/', views.seller_view, name='seller'),
    path('seller/signup/', views.seller_signup_view, name='seller_signup'),
    path('seller/logout/', views.seller_logout_view, name='seller_logout'),
    path('seller/add/', views.seller_add_view, name='seller_add'),
    path('seller/delete/<int:id>/', views.delete_view, name='delete'),
    path('seller/edit/<int:pk>/', views.edit_view, name='edit'),
]
