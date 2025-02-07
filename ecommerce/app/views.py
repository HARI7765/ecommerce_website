from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Medicine, MedicalEquipment  # Make sure MedicalEquipment model exists
from .forms import MedicineForm, MedicalEquipmentForm
from django.contrib.auth.models import User


#seller side

def seller_signin_view(request):
    if request.user.is_authenticated:
        return redirect('seller')
    username = None
    password = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return render(request, 'seller/sellersignin.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            return redirect('seller')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'seller/sellersignin.html')

def seller_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')
        print(username, password)

        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'seller/sellersignup.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff=True  
            user.save()
            messages.success(request,"account created successfully")
            return render(request, "seller/sellersignin.html")
    return render(request,"seller/sellersignup.html")

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
                return render(request, 'seller/selleradd.html')
            else:
                product = Product(name=name, price=price, offerprice=offerprice,image=image, dosage=dosage, description=description)
                product.save()
                messages.success(request, "Product added successfully!")
                return redirect( 'seller')
        return render(request,'seller/selleradd.html')

def delete_view(request, id):
    product = get_object_or_404(Product, pk=id)  # Get product by ID (or 404 if not found)
    product.delete()  
    messages.success(request, "Product deleted successfully!")  # Optional success message
    return redirect( 'seller')


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
    request.session.flush()
    logout(request)
    return render(request,'seller/sellersignin.html')