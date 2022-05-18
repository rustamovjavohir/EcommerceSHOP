from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

PAYMENT_TYPE = (
    ('KARTA ORQALI', 'Karta orqali'),
    ('NAQD PUL', 'Naqd pul'),
    ('ARALASH TO\'LOV', 'Aralash to\'lov'),
)


class Category(models.Model):
    name = models.CharField(_('category name'), max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(_("product name"), max_length=250, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_count = models.IntegerField(_('product count'), default=1)
    original_price = models.FloatField(_('original price'))
    selling_price = models.FloatField(_('selling price'), null=True, blank=True)
    code = models.CharField(_('product code'), max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.code}"

    class Meta:
        ordering = ['id']


class SoldProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sold_time = models.DateField(auto_now_add=True, blank=True)
    buy_count = models.IntegerField(default=1)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE, default='Naqd pul')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} {self.buy_count}"

    class Meta:
        ordering = ['id']
