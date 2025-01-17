from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import os
from .forms import CustomUserCreationForm, ProofUploadForm
from .forms import SignUpForm, UserProfileForForm

def signup_view(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Save user profile (proof)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Login the user after sign up
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard

    else:
        user_form = SignUpForm()
        profile_form = UserProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Send Email Verification
def send_verification_email(user):
    # Normally you'd generate a token or link for email verification.
    verification_link = f"http://yourdomain.com/verify-email/{user.id}"

    subject = 'Verify Your Email'
    message = f'Hi {user.username},\n\nPlease verify your email by clicking the following link: {verification_link}\n\nThank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)


# User Profile View (For uploading proof for verification)
@login_required
def upload_proof(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProofUploadForm(request.POST, request.FILES)
        if form.is_valid():
            proof = form.save(commit=False)
            proof.user = request.user  # Link the proof to the current user
            proof.save()
            messages.success(request, 'Proof uploaded successfully!')

            # Optionally, trigger email or approval process here
            return redirect('profile')
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = ProofUploadForm()

    return render(request, 'upload_proof.html', {'form': form})


# View to display user profile or dashboard
@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})


# Verify Email (Just an example, you would normally use tokens for email verification)
def verify_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        # In production, use tokens to verify the email
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_verified = True
        user_profile.save()

        messages.success(request, 'Your email has been verified successfully!')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid user ID or the user does not exist.')
        return redirect('signup')


