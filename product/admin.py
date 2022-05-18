from django.contrib import admin
from .models import SoldProducts, Product, Category
# Register your models here.

admin.site.register(SoldProducts)
admin.site.register(Product)
admin.site.register(Category)
