from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Core site pages
    path('', views.index, name='index'),  # Homepage
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('contact/', views.contact_view, name='contact'),
    
    # Shopping features
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    # Removed the incorrect path with product_details_view
    # Authentication
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='log'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin features
    path('ecommerce/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('ecommerce/add_product/', views.add_product_view, name='add_product'),
    path('ecommerce/edit_product/<int:id>/', views.edit_product_view, name='edit_product'),
    path('ecommerce/delete_product/<int:id>/', views.delete_product_view, name='delete_product'),
    path('product_details', views.product_detail_view, name='product_details'),
    path('ecommerce/manage_orders/', views.manage_orders_view, name='manage_orders'),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
