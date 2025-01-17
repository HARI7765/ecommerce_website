from django.urls import path
from . import views

urlpatterns = [
    # User Signup Route
    path('signup/', views.signup, name='signup'),

    # Email Verification Route
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),

    # User Profile Route
    path('profile/', views.profile, name='profile'),

    # Upload Proof Route (for user verification documents)
    path('upload-proof/', views.upload_proof, name='upload_proof'),
]
