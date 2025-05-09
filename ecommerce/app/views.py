from django.shortcuts import render, redirect
from .models import Product, Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from django.contrib import messages
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

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

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'signin.html', {'form': form})
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            if user.is_superuser:
                return redirect('admin_dashboard')  # use URL name here
            else:
                return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'signin.html')
# @login_required
def admin_dashboard_view(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue
    })
def register_admin_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
        if user.is_superuser:
         return redirect('admin_dashboard')  # still valid because the name is the same

        user.save()
        login(request, user)
        return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register_admin.html', {'form': form})
# @login_required
def add_product_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        category = request.POST['category']
        Product.objects.create(
            name=name,
            image=image,
            description=description,
            price=price,
            stock=stock,
            category=category
        )
        return redirect('admin_dashboard')
    return render(request, 'add_product.html')

# @login_required
def manage_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})
def logout_view(request):
    logout(request)
    return redirect('index')

def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         message = request.POST['message']
    return render(request,'contact.html')
        
