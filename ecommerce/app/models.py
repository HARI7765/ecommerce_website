from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.db.models.fields import CharField
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_detail/', default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(_("Order ID"), max_length=40,null=True)
    payment_id = models.CharField(_("Payment ID"), max_length=36,null=True)
    signature_id = models.CharField(_("Signature ID"), max_length=128,null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.quantity})"