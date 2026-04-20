from decimal import Decimal
import uuid
import requests
import random
from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category, CartItem, Order, Contact


# -------------------------------
# Custom Login Required Decorator
# -------------------------------
def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["next_url"] = request.get_full_path()
            return render(request, "login/login_required.html")
        return view_func(request, *args, **kwargs)
    return wrapper


# -------------------------------
# Home Page
# -------------------------------
def index(request):
    query = request.GET.get("q", "").strip()

    if query:
        categories = Category.objects.prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                )
            )
        )
    else:
        categories = Category.objects.prefetch_related("products").all()

    return render(request, "main/index.html", {"categories": categories})


# -------------------------------
# Product List
# -------------------------------
def product_list_view(request):
    products = Product.objects.all()
    return render(request, "products/products.html", {"products": products})


# -------------------------------
# Product Detail
# -------------------------------
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/product_detail.html", {
        "product": product,
        "in_stock": product.stock > 0
    })


# -------------------------------
# Cart
# -------------------------------
@custom_login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * Decimal("0.10")
    total = subtotal + tax

    return render(request, "orders/cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "cart_items_count": cart_items.count(),
    })


# -------------------------------
# Add to Cart (AJAX)
# -------------------------------
@custom_login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = CartItem.objects.filter(user=request.user).count()
        return JsonResponse({"success": True, "cart_count": cart_count})

    return JsonResponse({"success": False})


# -------------------------------
# Increase Quantity
# -------------------------------
@custom_login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect("cart")


# -------------------------------
# Decrease Quantity
# -------------------------------
@custom_login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")


# -------------------------------
# Remove from Cart
# -------------------------------
@custom_login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart")


# -------------------------------
# Orders
# -------------------------------
@custom_login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/orders.html", {"orders": orders})


# -------------------------------
# Checkout
# -------------------------------
@custom_login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            amount=item.product.price * item.quantity,
            status="PENDING",
            provider_order_id=str(uuid.uuid4())
        )

    cart_items.delete()
    messages.success(request, "Order placed!")
    return redirect("orders")


# -------------------------------
# Register
# -------------------------------
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Account created")
        return redirect("login")
    return render(request, "login/signup.html", {"form": form})


# -------------------------------
# Login
# -------------------------------
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            next_url = request.session.pop("next_url", None)
            return redirect(next_url or "index")
        messages.error(request, "Invalid login")
    return render(request, "login/signin.html")


# -------------------------------
# Logout
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect("index")


# -------------------------------
# Profile
# -------------------------------
@login_required
def profile_view(request):
    return render(request, "user/profile.html", {"user": request.user})


# -------------------------------
# Contact
# -------------------------------
def contact_view(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        messages.success(request, "Message sent!")
    return render(request, "contacts/contact.html")


# -------------------------------
# About
# -------------------------------
def about_view(request):
    return render(request, "about.html")


# -------------------------------
# Fetch Products from API
# -------------------------------
def fetch_medicines():
    medicine_images = [
        "https://cdn.pixabay.com/photo/2017/06/26/19/03/pills-2446809_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/29/09/32/pills-1869741_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/07/31/11/21/medicine-2557319_1280.jpg",
    ]
    supplement_images = [
        "https://cdn.pixabay.com/photo/2017/09/16/19/21/capsules-2755073_1280.jpg",
        "https://cdn.pixabay.com/photo/2018/03/27/08/05/protein-3264826_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/09/07/11/37/vitamins-1650114_1280.jpg",
    ]
    equipment_images = [
        "https://cdn.pixabay.com/photo/2015/07/02/10/29/stethoscope-828787_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/02/15/09/47/blood-pressure-monitor-2068489_1280.jpg",
        "https://cdn.pixabay.com/photo/2020/03/24/18/14/thermometer-4965092_1280.jpg",
    ]

    total_created = 0

    # --- Medicines from FDA API ---
    try:
        response = requests.get("https://api.fda.gov/drug/label.json?limit=10", timeout=20)
        response.raise_for_status()
        data = response.json().get("results", [])
        medicine_category, _ = Category.objects.get_or_create(name="Medicines")

        for item in data:
            openfda = item.get("openfda", {})
            name_list = openfda.get("brand_name") or openfda.get("generic_name") or ["Medicine"]
            name = name_list[0]
            desc_list = item.get("purpose") or item.get("indications_and_usage") or ["No description"]
            description = desc_list[0]

            _, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": Decimal(str(round(random.uniform(10, 200), 2))),
                    "stock": random.randint(10, 100),
                    "category": medicine_category,
                    "image": random.choice(medicine_images),
                }
            )
            if created:
                total_created += 1

    except requests.RequestException:
        pass

    # --- Supplements ---
    supplements = [
        ("Vitamin C 1000mg", "Boosts immunity and fights oxidative stress."),
        ("Vitamin D3", "Supports bone health and immune function."),
        ("Omega-3 Fish Oil", "Promotes heart and brain health."),
        ("Zinc Tablets", "Essential mineral for immunity and healing."),
        ("Magnesium", "Supports muscle and nerve function."),
        ("Multivitamin Daily", "Complete daily vitamin and mineral support."),
        ("Calcium + D3", "Strengthens bones and teeth."),
        ("Iron Supplement", "Prevents iron deficiency and fatigue."),
        ("B-Complex", "Supports energy metabolism and nervous system."),
        ("Biotin", "Promotes healthy hair, skin and nails."),
    ]
    supplement_category, _ = Category.objects.get_or_create(name="Supplement")
    for name, description in supplements:
        _, created = Product.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "price": Decimal(str(round(random.uniform(80, 300), 2))),
                "stock": random.randint(20, 80),
                "category": supplement_category,
                "image": random.choice(supplement_images),
            }
        )
        if created:
            total_created += 1

    # --- Equipment ---
    equipments = [
        ("Digital Thermometer", "Fast and accurate body temperature measurement."),
        ("Blood Pressure Monitor", "Easy home blood pressure tracking device."),
        ("Stethoscope", "Professional grade stethoscope for clinical use."),
        ("Pulse Oximeter", "Measures blood oxygen saturation instantly."),
        ("Glucometer", "Accurate blood glucose monitoring at home."),
        ("Nebulizer", "Delivers medication directly to the lungs."),
        ("Heating Pad", "Relieves muscle pain and stiffness."),
        ("Surgical Gloves", "Disposable latex-free protective gloves."),
        ("Face Mask N95", "High filtration respiratory protection mask."),
        ("First Aid Kit", "Complete emergency first aid supplies kit."),
    ]
    equipment_category, _ = Category.objects.get_or_create(name="Equipment")
    for name, description in equipments:
        _, created = Product.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "price": Decimal(str(round(random.uniform(100, 500), 2))),
                "stock": random.randint(10, 50),
                "category": equipment_category,
                "image": random.choice(equipment_images),
            }
        )
        if created:
            total_created += 1

    return total_created


# -------------------------------
# Fetch Products View
# -------------------------------
def fetch_products_view(request):
    count = fetch_medicines()
    messages.success(request, f"Done! Added {count} new products.")
    return redirect("products")