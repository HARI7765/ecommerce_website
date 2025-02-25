from django.shortcuts import render
from django.contrib.auth import login
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'app/home.html')

def signup(request):
    if request.method == 'POST':
        # Handle signup logic
        pass
    return render(request, 'app/user/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Add authentication logic here
        return render(request, 'app/user/signin.html')
    return render(request, 'app/user/signin.html')

def cart_view(request):
    return render(request, 'app/user/cart.html')

def add_to_cart(request, product_id):
    # Add to cart logic
    pass

def admin_page(request):
    return render(request, 'app/admin/admin_home.html')

def add_medicine(request):
    # Add medicine logic
    pass

def add_medical_equipment(request):
    # Add medical equipment logic
    pass

def seller_view(request):
    return render(request, 'app/seller/seller.html')

def seller_signup_view(request):
    return render(request, 'app/seller/sellersignup.html')

def seller_logout_view(request):
    logout(request)
    return redirect('seller:signin')

def seller_add_view(request):
    return render(request, 'app/seller/selleradd.html')

def delete_view(request, id):
    # Add product deletion logic here
    return redirect('seller:seller')

def edit_view(request, pk):
    return render(request, 'app/seller/selleradd.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Add authentication logic here
        return render(request, 'app/user/signin.html')  # Render signin page
    return render(request, 'app/user/signin.html')  # Render signin page
