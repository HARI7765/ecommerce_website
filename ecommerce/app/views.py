from django.shortcuts import render, redirect
from .models import Product, Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse  
from django.shortcuts import render, get_object_or_404
from .models import Product


    # Check if the user is authenticated
def index(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'index.html', {'categories': categories})    

# @login_required()
def cart_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        # Proceed with logic using user_id
    else:
        # Handle the case where the user is not authentlogicated
        user_id = None  # or handle it in a way that fits your app
        # You might want to redirect to a login page
        return redirect('login')  # Adjust 'login' to your login URL name
    
    # Continue with the rest of your cart logic
    return render(request, 'cart.html', {'user_id': user_id})


# @login_required
def checkout_view(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity,
                status='Pending'
            )
            item.delete()  # Clear cart after order
        return redirect('orders')  # Redirect to orders page
    return render(request, 'checkout.html')

# @login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def product_detail_view(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'product_view.html', {'product': product})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


from .models import Category

def login_view(request):
    if request.user.is_authenticated:
        return redirect_to_homepage(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            if user.is_superuser:
                return redirect('admin_dashboard')  # Use URL name
            else:
                return redirect_to_homepage(request)
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'signin.html')


def redirect_to_homepage(request):
    # Redirect to first available category
    first_category = Category.objects.first()
    if first_category:
        return redirect('index', id=first_category.id)
    else:
        messages.error(request, "No categories available.")
        return redirect('signin')  # or render a custom error page
    

# @login_required
def admin_dashboard_view(request):
    products = Product.objects.all()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products': products,
    })


def signup(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Corrected line to use create_user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('log')  

    return render(request, "signup.html")# @login_required


def add_product_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')

        # Validate category
        category = get_object_or_404(Category, id=category_id)

        # Validate and convert numeric fields
        try:
            price = float(price)
            stock = int(stock)
        except (ValueError, TypeError):
            # handle invalid inputs gracefully
            return render(request, 'add_product.html', {
                'categories': Category.objects.all(),
                'error': 'Price must be a number and stock must be an integer.'
            })

        # Create the product
        Product.objects.create(
            name=name,
            image=image,
            description=description,
            price=price,
            stock=stock,
            category=category
        )

        return redirect('admin_dashboard')

    # GET request
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    return render(request, 'product_detail.html', {'product': product})

def edit_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.image = request.FILES.get('image', product.image)  # Keep old image if new one not provided
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.category_id = request.POST.get('category')

        # Validate and convert numeric fields
        try:
            product.price = float(product.price)
            product.stock = int(product.stock)
        except (ValueError, TypeError):
            # handle invalid inputs gracefully
            return render(request, 'edit_product.html', {
                'product': product,
                'categories': Category.objects.all(),
                'error': 'Price must be a number and stock must be an integer.'
            })

        product.save()
        return redirect('admin_dashboard')

    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})

def delete_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_product.html', {'product': product})


# @login_required
def manage_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})


def logout_view(request):
    logout(request)
    return redirect('index')

def contact_view(request):
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     message = request.POST['message']
    return render(request,'contact.html')


        
