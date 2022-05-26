from rest_framework import serializers
from .models import Product, SoldProducts, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SoldProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldProducts
        fields = '__all__'
        # depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # depth = 1

# this is test branch
