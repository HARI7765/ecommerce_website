from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .models import Product  # Assuming a Product model exists
import logging
from django.contrib.auth import logout


logger = logging.getLogger(__name__)

# Basic Views
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'app/home.html')

# Authentication Views
def signup(request):  # User registration view
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password or len(password) < 8:
            messages.error(request, "Passwords do not match.")
            return render(request, 'app/user/signup.html')  # Make sure this path is correct

        # Create a new user with additional validation
        user = User.objects.create_user(username=username, email=email, password=password)  # Ensure unique username
        user.save()

        # Log in the user
        login(request, user)
        messages.success(request, "Registration successful. You are now signed in. Please check your email for verification.")
        return redirect('app:home')  # Corrected redirect

    return render(request, 'app/user/signup.html')

def signin(request):  # User sign-in view
    logger.debug("Sign-in attempt for user: %s", request.POST.get('username'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully signed in.")
            logger.debug("User %s signed in successfully.", username)
            return redirect('app:home')  # Redirect to home after successful sign-in
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'app/user/signin.html')

# Cart Management Views
def view_cart(request):  # View shopping cart
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render(request, 'app/user/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):  # Add item to cart
    cart = request.session.get('cart', {})
    product_id = str(product_id)  # session keys must be strings
    
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    request.session['cart'] = cart
    messages.success(request, "Item added to cart")
    
    return redirect('app:cart')  # Redirect to the cart page

# Admin Views
def admin_page(request):  # Admin dashboard view
    return render(request, 'app/admin/admin_home.html')

def add_medicine(request):  # Add new medicine view
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Create a new Medicine instance (assuming a Medicine model exists)
        medicine = Medicine(name=name, description=description, price=price)
        medicine.save()

        messages.success(request, "Medicine added successfully.")
        return redirect('app:admin_page')

    return render(request, 'app/admin/add_medicine.html')

def add_medical_equipment(request):  # Add new medical equipment view
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Create a new MedicalEquipment instance (assuming a MedicalEquipment model exists)
        equipment = MedicalEquipment(name=name, description=description, price=price)
        equipment.save()

        messages.success(request, "Medical equipment added successfully.")
        return redirect('app:admin_page')

    return render(request, 'app/admin/add_medical_equipment.html')

# Seller Views
def seller_signup_view(request):  # Seller registration view
    if request.method == 'POST':
        # Logic for seller signup
        pass
    return render(request, 'app/seller/sellersignup.html')

def seller_view(request):  # Seller dashboard view
    return render(request, 'app/seller/seller.html')

def seller_add_view(request):  # Add seller's product view
    if request.method == 'POST':
        # Logic for adding a seller's product
        pass
    return render(request, 'app/seller/selleradd.html')

def seller_logout_view(request):
    logout(request)
    return redirect('seller:signin')

def delete_view(request, id):  # Delete seller's product view
    # Add product deletion logic here
    return redirect('seller:seller')

def edit_view(request, pk):  # Edit seller's product view
    return render(request, 'app/seller/selleradd.html')

def seller_view(request):
    # Render the seller's home page/dashboard
    return render(request, 'app/seller/seller.html')

def seller_signup_view(request):
    if request.method == 'POST':
        # Handle form submission for seller registration
        pass
    return render(request, 'app/seller/sellersignup.html')

def seller_logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('app:home')  # Redirect to the home page or sign-in page after logout

def seller_add_view(request):
    if request.method == 'POST':
        # Handle product addition (e.g., saving a new product)
        pass
    return render(request, 'app/seller/selleradd.html')

def delete_view(request, id):
    # Get the product to delete
    product = get_object_or_404(Product, id=id)
    
    # Optional: Check if the current seller owns the product
    if product.seller != request.user:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('seller:home')
    
    # Delete the product and provide feedback
    product.delete()
    messages.success(request, "Product successfully deleted.")
    return redirect('seller:home')

def edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Handle form submission for editing the product
        pass
    
    return render(request, 'app/seller/selleradd.html', {'product': product})
