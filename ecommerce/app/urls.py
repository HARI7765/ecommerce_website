from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin Panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/add-product/', views.admin_add_product, name='admin_add_product'),
    path('admin-panel/delete-product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('admin-panel/toggle-user/<int:user_id>/', views.admin_toggle_user, name='admin_toggle_user'),
    
    # Home
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),

    # Products
    path('products/', views.product_list_view, name='products'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('fetch-products/', views.fetch_products_view, name='fetch_products'),

    # Search
    path('search/', views.index, name='search'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Orders
    path('orders/', views.orders_view, name='orders'),
    path('checkout/', views.checkout, name='checkout'),

    path('checkout/', views.checkout, name='checkout'),
 path('payment/success/', views.payment_success, name='payment_success'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Contact
    path('contact/', views.contact_view, name='contact'),

    # About
    path('about/', views.about_view, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)