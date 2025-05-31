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
from decimal import Decimal
from . forms import ProductForm
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Product, CartItem, Order
import uuid
from django.http import JsonResponse
from functools import wraps
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact


# Custom decorator for login required with oops page
def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Store the original URL they were trying to access
            request.session['next_url'] = request.get_full_path()
            return render(request, 'login/login_required.html', {
                'message': 'Oops! You need to login to access this page.',
                'redirect_url': request.get_full_path(),
                'page_title': 'Login Required'
            })
        return view_func(request, *args, **kwargs)
    return wrapper

# Custom decorator for admin required with oops page
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('log')  # Redirect to login
        elif not request.user.is_superuser:
            return render(request, 'admin/admin_required.html', ...)
        return view_func(request, *args, **kwargs)
    return wrapper

def index(request, id=None):
    # Handle product ID if provided
    product_id = id
    
    # Handle search query if provided
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # Get all categories with their products
    categories = Category.objects.prefetch_related('products').all()
    
    context = {
        'product_id': product_id,
        'products': products,
        'categories': categories,
        'query': query
    }
    return render(request, 'main/index.html', context)

def about_view(request):
    """
    View for the About page.
    """
    return render(request, 'main/about.html')

@custom_login_required
def cart_view(request):
    # Get all cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_count = sum(item.quantity for item in cart_items)
    
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * Decimal('0.10')  # 10% tax
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'orders/cart.html', context)

@custom_login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def product_detail_view(request, id):
    # Get a single product object instead of a queryset
    product = Product.objects.get(id=id)
    
    # Check if product is in stock
    in_stock = product.stock > 0
    
    # Check if the product is in the user's cart (if user is authenticated)
    cart_product_ids = []
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_product_ids = [item.product.id for item in cart_items]
    
    # Similar for wishlist if you have that functionality
    wishlist_product_ids = []
    
    context = {
        'product': product,
        'in_stock': in_stock,
        'cart_product_ids': cart_product_ids,
        'wishlist_product_ids': wishlist_product_ids,
    }
    
    return render(request, 'products/product_view.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Check if there's a next URL to redirect to
            next_url = request.session.get('next_url')
            if next_url:
                del request.session['next_url']
                return redirect(next_url)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', {'form': form})

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
            
            # Handle next URL redirect
            next_url = request.session.get('next_url')
            if next_url:
                del request.session['next_url']
                return redirect(next_url)
            
            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin_dashboard')  # Using URL name
            else:
                return redirect_to_homepage(request)
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login/signin.html')

def redirect_to_homepage(request):
    # Redirect to first available category
    first_category = Category.objects.first()
    if first_category:
        return redirect('index', id=first_category.id)
    else:
        messages.error(request, "No categories available.")
        return redirect('signin')
    
@admin_required
def admin_dashboard_view(request):
    products = Product.objects.all()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'admin/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products': products,
    })
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('log')
        elif not request.user.is_superuser:
            return render(request, 'admin/admin_required.html', {
                'message': 'You need admin privileges to access this page.'
            })
        return view_func(request, *args, **kwargs)
    return wrapper

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
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            
            # Check if there's a next URL to redirect to after signup
            next_url = request.session.get('next_url')
            if next_url:
                login(request, user)  # Auto login after signup
                del request.session['next_url']
                return redirect(next_url)
            
            return redirect('log')  

    return render(request, "login/signup.html")

@admin_required
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
            return render(request, 'products/add_product.html', {
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

        return redirect('admin_dashboard')  # Use the URL name

    # GET request
    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@admin_required
@require_http_methods(["GET", "POST"])
def edit_product_view(request, id):
    """
    View for editing an existing product.
    Requires admin privileges and handles both GET and POST requests.
    """
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' was updated successfully.")
            return redirect('admin/admin_dashboard')
    else:
        form = ProductForm(instance=product)
    
    categories = Category.objects.all()
    
    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product,
        'categories': categories
    })

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})

@admin_required
def delete_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' has been deleted successfully.")
        return redirect('admin_dashboard')
    return render(request, 'products/delete_product.html', {'product': product})

@admin_required
def manage_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'orders/manage_orders.html', {'orders': orders})

@custom_login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@custom_login_required
def profile_view(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user.username,
        'email': user.email,
    }
    return render(request, 'user/profile.html', context)



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        # Send email to website contact
        send_mail(
            subject=f'New Contact Form Submission from {name}',
            message=f"Name: {name}\nEmail: {email}\nMessage: {message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test1project11@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'contacts/contact.html')
    return render(request, 'contacts/contact.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    # Check if product is in cart
    cart_product_ids = []
    cart_items_count = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_product_ids = [item.product.id for item in cart_items]
        cart_items_count = sum(item.quantity for item in cart_items)
    
    context = {
        'product': product,
        'categories': categories,
        'in_stock': product.stock > 0,
        'cart_product_ids': cart_product_ids,
        'cart_items_count': cart_items_count,
    }
    
    # If it's a POST request, handle adding to cart
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Store the current URL for redirect after login
            request.session['next_url'] = request.get_full_path()
            return render(request, 'login/oops_login_required.html', {
                'message': 'Oops! Please login to add items to your cart.',
                'redirect_url': request.get_full_path(),
                'page_title': 'Login Required',
                'action': 'add items to cart'
            })
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if already in cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        # If not created, update the quantity
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"{product.name} added to your cart!")
        return redirect('cart')
    
    return render(request, 'products/product_detail.html', context)

@custom_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Don't add if out of stock
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('product_detail', product_id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if already in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    # If not created, update the quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart!")
    
    # If the request is AJAX, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('cart')

@custom_login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')

@custom_login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    # Check if increasing quantity is possible (stock availability)
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.warning(request, f"Sorry, only {cart_item.product.stock} items available in stock.")
    
    return redirect('cart')

@custom_login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    
    return redirect('cart')

@custom_login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Your cart has been cleared.")
    return redirect('cart')

@custom_login_required
def checkout(request):
    # Get all cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate subtotal
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    # Calculate shipping cost - free over ₹500, otherwise ₹50
    shipping_cost = Decimal('0.00') if subtotal >= 500 else Decimal('50.00')
    
    # Calculate tax (5% of subtotal)
    tax_amount = subtotal * Decimal('0.05')
    
    # Calculate total
    total = subtotal + shipping_cost + tax_amount
    
    if request.method == 'POST':
        # Process the order
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        state = request.POST.get('state')
        country = request.POST.get('country')
        
        # Validate form data
        if not all([first_name, last_name, email, phone, address, city, postal_code, state, country]):
            messages.error(request, 'Please fill all the required fields.')
            return redirect('checkout')
        
        # Create new order for each cart item
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                amount=float(item.product.price * item.quantity),
                status='PENDING',
                provider_order_id=str(uuid.uuid4())[:40]
            )
            
            # Update product stock
            product = item.product
            product.stock -= item.quantity
            product.save()
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation')
    
    context = {
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax_amount': tax_amount,
        'total': total
    }
    
    return render(request, 'orders/checkout.html', context)

@custom_login_required
def order_confirmation(request):
    # Get recent orders for the current user
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_orders': recent_orders,
        'cart_items_count': CartItem.objects.filter(user=request.user).count()
    }
    
    return render(request, 'orders/order_confirmation.html', context)