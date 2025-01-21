from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d&rk5og6)#)dxtkp6+#uld7_c(nj2_1flp7dn%7+7-lubio1v%'  # Set this to a secure value in production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add production domain(s) when deploying

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Your app should be listed here
    # Other apps like 'django.contrib.sites', 'rest_framework' can be added as needed.
]

MIDDLEWARE = [# ...existing code...
DEBUG = False  # Set to False in production
# ...existing code...
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',  # Replace with your database name
        'USER': 'your_db_user',   # Replace with your username
        'PASSWORD': 'your_db_password',  # Replace with your password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Ensure you have this for local development
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Make sure you create this directory
]

# If you're in production, use:
# STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (for uploaded images, documents, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Email settings (for account verification, notifications)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Gmail as an example
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your_email_password'  # Replace with your email password

# For sending email from an e-commerce website (e.g., order confirmation, verification)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# File upload handling (image or proof uploads for users/products)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB limit for file uploads

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Security settings
SECURE_SSL_REDIRECT = False  # Set to True for production to force HTTPS
CSRF_COOKIE_SECURE = False  # Set to True for production
SESSION_COOKIE_SECURE = False  # Set to True for production

# X-Content-Type-Options header
SECURE_CONTENT_TYPE_NOSNIFF = True

# Strict-Transport-Security header (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Cross-Origin Resource Sharing (CORS) settings if using frontend API
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']  # Modify for your frontend origin
