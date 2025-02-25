from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'app/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'app/user/signup.html')  # Corrected render call

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log in the user
        login(request, user)
        messages.success(request, "Registration successful. You are now signed in.")
        return redirect('home')

    return render(request, 'app/user/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully signed in.")
            return redirect('app:home')  # Redirect to home after successful sign-in
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'app/user/signin.html')

def cart_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be signed in to proceed to checkout.")
        return redirect('app:signin')  # Redirect to sign-in page if not authenticated

    return render(request, 'app/user/cart.html')

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be signed in to add items to your cart.")
        return redirect('app:signin')  # Redirect to sign-in page if not authenticated

    # Logic to add the product to the cart

    # Logic to add the product to the cart
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    messages.success(request, "Product added to cart.")
    return redirect('app:cart')  # Redirect to cart view

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
