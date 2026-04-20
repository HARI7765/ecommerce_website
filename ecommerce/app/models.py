from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .constants import PaymentStatus


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(
        default="https://via.placeholder.com/150",
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Payment Status"),
        max_length=50,
        default=PaymentStatus.PENDING,
        choices=[
            (PaymentStatus.PENDING, "Pending"),
            (PaymentStatus.COMPLETED, "Completed"),
            (PaymentStatus.FAILED, "Failed"),
        ],
    )
    provider_order_id = models.CharField(
        _("Provider Order ID"),
        max_length=40,
        null=True,
        blank=True
    )
    payment_id = models.CharField(
        _("Payment ID"),
        max_length=36,
        null=True,
        blank=True
    )
    signature_id = models.CharField(
        _("Signature ID"),
        max_length=128,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"