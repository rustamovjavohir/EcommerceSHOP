from rest_framework.routers import DefaultRouter

from .views import ProductViewset, CategoryViewset

routers = DefaultRouter()

routers.register(f'product', ProductViewset, basename='product')
routers.register(f'category', CategoryViewset, basename='category')
# routers.register(f'soldproduct', SoldProductViewset, basename='soldproduct')

urlpatterns = routers.urls
