from django.urls import path
from .views import (
    register_view,
    login_view,
    index,
    cart_view,
    checkout_view,
    orders_view,
    product_detail_view,
    admin_dashboard_view,
    add_product_view,
    manage_orders_view
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),  # Homepage displaying products
    path('cart/', cart_view, name='cart'),  # Cart page
    path('checkout/', checkout_view, name='checkout'),  # Checkout page
    path('orders/', orders_view, name='orders'),  # User orders page
    path('product/<int:id>/', product_detail_view, name='product_detail'),  # Product detail page
    path('register/', register_view, name='register'),  # User registration
    path('login/', login_view, name='login'),  # User login
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout page
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),  # Admin dashboard
    path('admin/add_product/', add_product_view, name='add_product'),  # Admin add product
    path('admin/manage_orders/', manage_orders_view, name='manage_orders'),  # Admin manage orders
]
