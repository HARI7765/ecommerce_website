from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Medicine, MedicalEquipment
from .forms import MedicineForm, MedicalEquipmentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Seller side

def seller_signin_view(request):
    if request.user.is_authenticated:
        return redirect('seller')
    username = None
    password = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return render(request, 'seller/sellersignin.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            return redirect('seller')
        
        messages.error(request, 'Invalid credentials')
    
    return render(request, 'seller/sellersignin.html')

def seller_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True  
            user.save()
            messages.success(request, "Account created successfully")
            return render(request, "seller/sellersignin.html")  # Redirect to signin page
    
    return render(request, 'seller/sellersignup.html')  # Render signup page

def seller_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        offerprice = request.POST.get('offerprice')
        image = request.FILES.get('image')
        dosage = request.POST.get('dosage')
        description = request.POST.get('description')

        if not name or not price or not offerprice or not image or not dosage or not description:
            messages.error(request, "All fields are required!")
            return render(request, 'seller/selleradd.html')  # Render add product page
        
        messages.success(request, "Product added successfully!")
        return redirect('seller')
    
    return render(request, 'seller/selleradd.html')  # Render add product page

def delete_view(request, id):
    messages.success(request, "Product deleted successfully!")  # Optional success message
    return redirect('seller')

def edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Ensure product exists

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.offerprice = request.POST.get('offerprice')
        product.dosage = request.POST.get('dosage')
        product.description = request.POST.get('description')

        image = request.FILES.get('image')  # Check for new image
        if image:
            product.image = image  # Update only if a new image is uploaded

        product.save()  # Save the updated instance properly
        return redirect('seller')

    return render(request, 'seller/editseller.html', {'editor': product})

def seller_logout_view(request):
    request.session.flush()  # Clear session data
    logout(request)
    return render(request, 'seller/sellersignin.html')

def index(request):
    medicines = Medicine.objects.all()
    equipment = MedicalEquipment.objects.all()
    products = list(medicines) + list(equipment)
    return render(request, 'index.html', {'products': products})

def home(request):
    medicines = Medicine.objects.all()
    equipment = MedicalEquipment.objects.all()
    return render(request, 'app/home.html', {
        'medicines': medicines,
        'equipment': equipment
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'app/user/signin.html')  # Render signin page

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully")
            return redirect('signin')  # Redirect to signin page

    return render(request, 'app/signup.html')  # Render signup page

@login_required
def admin_page(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page")
        return redirect('home')
    
    medicines = Medicine.objects.all()
    equipment = MedicalEquipment.objects.all()
    return render(request, 'app/admin_page.html', {
        'medicines': medicines,
        'equipment': equipment
    })

@login_required
def cart_view(request):
    return render(request, 'app/cart.html')

def add_to_cart(request, product_id):
    """
    Add a product to the user's shopping cart.
    Redirects to signin page if user is not authenticated.
    """
    if not request.user.is_authenticated:
        messages.info(request, "Please sign in to add items to your cart")
        return redirect('signin')
        
    try:
        product = Medicine.objects.get(id=product_id)
        cart = request.session.get('cart', {})
        
        # Add product to cart or increment quantity
        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1
        
        request.session['cart'] = cart
        messages.success(request, f"{product.name} added to cart!")
    except Medicine.DoesNotExist:
        messages.error(request, "Product not found")
    
    return redirect('cart_view')

@login_required
def add_medicine(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to add medicines")
        return redirect('home')
        
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('admin_page')
    else:
        form = MedicineForm()
    return render(request, 'app/add_medicine.html', {'form': form})

@login_required
def add_medical_equipment(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to add medical equipment")
        return redirect('home')
        
    if request.method == 'POST':
        form = MedicalEquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical equipment added successfully!')
            return redirect('admin_page')
    else:
        form = MedicalEquipmentForm()
    return render(request, 'app/add_medical_equipment.html', {'form': form})

@login_required
def seller_view(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page")
        return redirect('home')
    
    # Logic to retrieve seller-specific data can be added here
    return render(request, 'seller/seller_home.html')  # Render the seller home page
