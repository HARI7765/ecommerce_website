
from .models import *

from django.contrib import admin
from .models import Category, Product, Order, CartItem, Contact

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Contact)