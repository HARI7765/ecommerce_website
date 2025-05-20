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




    # Check if the user is authenticated
def index(request, id=None):
    # Handle product ID if provided
    product_id = id
    
    # Handle search query if provided
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter()
        Q(name__icontains=query) | Q(description__icontains=query)
    
    # Get all categories with their products
    categories = Category.objects.prefetch_related('products').all()
    
    context = {
        'product_id': product_id,
        'products': products,
        'categories': categories,
        'query': query
    }
    return render(request, 'index.html', context)

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


# @login_required
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
    # Uncomment and modify if you have a wishlist model
    # if request.user.is_authenticated:
    #     wishlist_items = Wishlist.objects.filter(user=request.user)
    #     wishlist_product_ids = [item.product.id for item in wishlist_items]
    
    context = {
        'product': product,
        'in_stock': in_stock,
        'cart_product_ids': cart_product_ids,
        'wishlist_product_ids': wishlist_product_ids,
    }
    
    return render(request, 'product_view.html', context)

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

@login_required
@require_http_methods(["GET", "POST"])
def edit_product_view(request, id):
    """
    View for editing an existing product.
    Requires login and handles both GET and POST requests.
    """
    # Get the product or return 404
    product = get_object_or_404(Product, id=id)
    
    # Check if the user has permission to edit products
    if not request.user.has_perm('products.change_product'):
        messages.error(request, "You don't have permission to edit products.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        # Create form instance with POST data and files, instance is the existing product
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            # Form will handle all validation including price and stock
            form.save()
            messages.success(request, f"Product '{product.name}' was updated successfully.")
            return redirect('admin_dashboard')
    else:
        # Create form pre-populated with product data for GET request
        form = ProductForm(instance=product)
    
    # Get all categories for the form dropdown
    categories = Category.objects.all()
    
    # Render the template with the form and categories
    return render(request, 'edit_product.html', {
        'form': form,
        'product': product,
        'categories': categories
    })



def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

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

# @login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user.username,
        'email': user.email,

    }
    return render(request, 'profile.html',context)



def contact_view(request):
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     message = request.POST['message']
    return render(request,'contact.html')


        
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
            messages.warning(request, "Please log in to add items to your cart.")
            return redirect('log')
        
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
    
    return render(request, 'product_detail.html', context)

@login_required
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
    
    return render(request, 'cart.html', context)

@login_required
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

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    # Check if increasing quantity is possible (stock availability)
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.warning(request, f"Sorry, only {cart_item.product.stock} items available in stock.")
    
    return redirect('cart')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    
    return redirect('cart')

@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Your cart has been cleared.")
    return redirect('cart')

@login_required
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
                provider_order_id=str(uuid.uuid4())[:40]  # Generate a unique order ID
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
    
    return render(request, 'checkout.html', context)

@login_required
def order_confirmation(request):
    # Get recent orders for the current user
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_orders': recent_orders,
        'cart_items_count': CartItem.objects.filter(user=request.user).count()
    }
    
    return render(request, 'order_confirmation.html', context)