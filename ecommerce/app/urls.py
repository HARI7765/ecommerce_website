from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin dashboard and features
    path('register/admin/', views.register_admin_view, name='register_admin'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/add_product/', views.add_product_view, name='add_product'),
    path('admin/manage_orders/', views.manage_orders_view, name='manage_orders'),

    path('contact/', views.contact_view, name='contact'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
