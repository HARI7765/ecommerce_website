from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Signup page view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('signin')
        else:
            messages.error(request, 'There was an error with your signup. Please check your form.')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

# Signin page view
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    return render(request, 'signin.html')

# Index page view
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

# Cart view to display added items
def cart(request):
    cart_items = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart_items': cart_items})

# Add to cart view
def add_to_cart(request, product_id):
    # You can replace product_id with actual product data in a real app
    product = {'id': product_id, 'name': f'Product {product_id}', 'price': 5.00}  # Dummy data for illustration
    cart = request.session.get('cart', [])
    cart.append(product)
    request.session['cart'] = cart  # Save updated cart in session
    return redirect('cart')  # Redirect to cart page
