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
        return redirect('app:home')  # Updated redirect to use namespaced URL

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

def seller_signup_view(request):
    if request.method == 'POST':
        # Logic for seller signup
        pass
    return render(request, 'app/seller/sellersignup.html')

def view_cart(request):
    """View the current shopping cart"""
    # Get the cart from the session or initialize an empty one
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    # Get the details of each item in the cart
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, product_id):
    """Add a product to the cart"""
    # Get the cart from the session or initialize an empty one
    cart = request.session.get('cart', {})
    
    # Convert to string because session keys must be strings
    product_id = str(product_id)
    
    # Increment quantity if product is already in cart, otherwise add it
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    # Save the cart back to the session
    request.session['cart'] = cart
    messages.success(request, "Item added to cart")
    
    return redirect('product_list')  # Redirect to product list page

def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    # Get the cart from the session
    cart = request.session.get('cart', {})
    
    # Convert to string because session keys must be strings
    product_id = str(product_id)
    
    # Remove the product if it's in the cart
    if product_id in cart:
        del cart[product_id]
        # Save the updated cart back to the session
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart")
    
    return redirect('view_cart')

def update_cart(request, product_id):
    """Update the quantity of a product in the cart"""
    # This would be called from a form submission
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[product_id] = quantity
        else:
            # Remove item if quantity is 0
            if product_id in cart:
                del cart[product_id]
        
        request.session['cart'] = cart
        messages.success(request, "Cart updated")
    
    return redirect('view_cart')

def clear_cart(request):
    """Clear all items from the cart"""
    if 'cart' in request.session:
        del request.session['cart']
        messages.success(request, "Cart cleared")
    
    return redirect('view_cart')
def admin_page(request):
    return render(request, 'app/admin/admin_home.html')

def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Create a new Medicine instance
        medicine = Medicine(name=name, description=description, price=price)
        medicine.save()

        messages.success(request, "Medicine added successfully.")
        return redirect('app:admin_page')  # Redirect to admin page after adding

    return render(request, 'app/admin/add_medicine.html')  # Render the add medicine form

def add_medical_equipment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Create a new MedicalEquipment instance
        equipment = MedicalEquipment(name=name, description=description, price=price)
        equipment.save()

        messages.success(request, "Medical equipment added successfully.")
        return redirect('app:admin_page')  # Redirect to admin page after adding

    return render(request, 'app/admin/add_medical_equipment.html')  # Render the add equipment form

def seller_view(request):
    return render(request, 'app/seller/seller.html')

def seller_logout_view(request):
    logout(request)
    return redirect('seller:signin')

def seller_add_view(request):
    if request.method == 'POST':
        # Logic for adding a seller's product
        pass
    return render(request, 'app/seller/selleradd.html')

def delete_view(request, id):
    # Add product deletion logic here
    return redirect('seller:seller')

def edit_view(request, pk):
    return render(request, 'app/seller/selleradd.html')
