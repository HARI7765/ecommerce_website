# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Signup page view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('signin')  # Redirect to sign-in page after successful signup
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
    # Redirect to signin if user is already logged in
    if request.user.is_authenticated:
        return redirect('home')  # Or redirect to any logged-in page (e.g., dashboard)
    return render(request, 'index.html')
