from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Medicine, MedicalEquipment  # Make sure MedicalEquipment model exists
from .forms import MedicineForm, MedicalEquipmentForm

# Home view (basic version)
def home(request):
    return render(request, 'home.html')

# Index view (product listing)
def index(request):
    medicines = Medicine.objects.all()
    medical_equipment = MedicalEquipment.objects.all()
    return render(request, 'index.html', {
        'medicines': medicines,
        'medical_equipment': medical_equipment
    })

# Authentication views
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

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    return render(request, 'signin.html')

# Cart functionality
def cart(request):
    return render(request, 'cart.html', {
        'cart_items': request.session.get('cart', [])
    })
def cart_view(request):
    cart_items = request.session.get('cart', [])
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)  # Multiply by quantity
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'some_value': total_price
    })


def add_to_cart(request, product_id):
    try:
        product = Medicine.objects.get(id=product_id)
        product_type = 'medicine'
    except Medicine.DoesNotExist:
        try:
            product = MedicalEquipment.objects.get(id=product_id)
            product_type = 'equipment'
        except MedicalEquipment.DoesNotExist:
            messages.error(request, "Product not found")
            return redirect('index')  # or some error page
    
    cart = request.session.get('cart', [])
    
    product_in_cart = next((item for item in cart if item['id'] == product_id), None)
    
    if product_in_cart:
        product_in_cart['quantity'] += 1
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'type': product_type,
            'quantity': 1
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

def add_medical_equipment(request):
    if request.method == 'POST':
        form = MedicalEquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = MedicalEquipmentForm()
    return render(request, 'add_medical_equipment.html', {'form': form})
def admin_page(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')
    
    medicines = Medicine.objects.all()
    equipment = MedicalEquipment.objects.all()
    return render(request, 'admin_page.html', {
        'medicines': medicines,
        'equipment': equipment
    })
