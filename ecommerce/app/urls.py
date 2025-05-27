from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from app.views import product_list_view

urlpatterns = [
    # Core site pages
    path('', views.index, name='home'),  # Homepage
    path('index/', views.index, name='index'),  # Homepage
    path('index/<int:id>/', views.index, name='index'),  # Homepage
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    

    # Product listing
    path('products/', views.product_list_view, name='product'),


    # Cart and Checkout
    path('cart/', views.cart_view, name='cart'),
    path('orders/', views.orders_view, name='orders'),



        # Cart views
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),


    #payments and shipping



    # Authentication
    path('oops/', views.custom_login_required, name='oops'),
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='log'),
    
    path('logout/', views.logout_view, name='logout'),

    
    # Admin features
    path('ecommerce/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('ecommerce/add_product/', views.add_product_view, name='add_product'),
    path('ecommerce/edit_product/<int:id>/', views.edit_product_view, name='edit_product'),
    path('ecommerce/delete_product/<int:id>/', views.delete_product_view, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('ecommerce/manage_orders/', views.manage_orders_view, name='manage_orders'),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
