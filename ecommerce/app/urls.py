from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'app'

urlpatterns = [
    # Basic URLs
    path('', views.index, name='index'),  # Home page
    path('cart/', views.view_cart, name='cart'),  # Cart view
    path('home/', views.home, name='home'),  # Home page after login/sign-in
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),  # User registration
    path('signin/', views.signin, name='signin'),  # User sign-in
    path('login/', LoginView.as_view(), name='login'),  # Django default login view
    path('logout/', LogoutView.as_view(), name='logout'),  # Django default logout view
    
    # Cart Management URLs
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    
    # Admin/Product Management URLs
    path('admin_page/', views.admin_page, name='admin_page'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),  # Add new medicine
    path('add_medical_equipment/', views.add_medical_equipment, name='add_medical_equipment'),  # Add new medical equipment
    
    # Seller URLs
    path('seller/', include(('app.urls_seller', 'seller'), namespace='seller')),  # Seller paths
]
