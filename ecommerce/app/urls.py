from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Add this line to route the root URL to the 'index' view
    path('', views.index, name='index'),  # Homepage displaying products

    # Your other URL patterns
    path('cart/', views.cart_view, name='cart'),  # Cart page
    path('checkout/', views.checkout_view, name='checkout'),  # Checkout page
    path('orders/', views.orders_view, name='orders'),  # User orders page
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),  # Product detail page
    path('register/', views.register_view, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),  # Admin dashboard
    path('admin/add_product/', views.add_product_view, name='add_product'),  # Admin add product
    path('admin/manage_orders/', views.manage_orders_view, name='manage_orders'),  # Admin manage orders
    path('contact/',views.contact_view, name='contact'),  # Contact page
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
