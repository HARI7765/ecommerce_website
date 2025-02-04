from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Medicine
from .forms import MedicineForm, MedicalEquipmentForm

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please login.')
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Signin view
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')  # Make sure 'home' exists in urls.py
        messages.error(request, 'Invalid credentials')
    return render(request, 'signin.html')

# Home view
def index(request):
    medicines = Medicine.objects.all()
    return render(request, 'index.html', {'medicines': medicines})

# Cart view
def cart(request):
    return render(request, 'cart.html', {
        'cart_items': request.session.get('cart', [])
    })

# Add to cart with quantity handling and validation
def add_to_cart(request, product_id):
    product = get_object_or_404(Medicine, id=product_id)
    cart = request.session.get('cart', [])
    
    # Check if product is already in cart
    product_in_cart = next((item for item in cart if item['id'] == product_id), None)
    
    if product_in_cart:
        # Increase quantity if the product is already in the cart
        product_in_cart['quantity'] += 1
    else:
        # Add new product to the cart
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1  # Start with quantity 1
        })
    
    request.session['cart'] = cart
    return redirect('cart')

# Admin views
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

def admin_page(request):
    return render(request, 'admin_page.html')

