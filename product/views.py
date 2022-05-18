from collections import defaultdict

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product, SoldProducts, Category
from .serializers import ProductSerializer, SoldProductsSerializer, CategorySerializer
from .utils import ProductPagination, SoldProductPagination


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    # permission_classes = [AllowAny, ]
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = ProductPagination
    parser_classes = [JSONParser, ]

    @swagger_auto_schema(operation_summary="Mahsulotni shrix code bilan qoshish")
    @action(methods=['post'], detail=False, url_path='addproduct', url_name='addproduct')
    def add_product(self, request, *args, **kwargs):
        product_code = request.data.get('code').lower()
        obj = self.get_queryset().filter(code__icontains=product_code).first()
        if obj:
            obj.product_count += 1
            obj.save()
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'message': 'product not found'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Mahsulotlar royhatini chop etish')
    def list(self, request, *args, **kwargs):
        return super(ProductViewset, self).list(self, request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Yangi Mahsulot kirish")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mahsulot malumotlarini yangilash")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mahsulot malumotlarini qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Mahsulot malumotlarini o'chirish")
    def destroy(self, request, *args, **kwargs):
        return super(ProductViewset, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Mahsulot haqidagi malumotlarini chop etish (retrieve)")
    def retrieve(self, request, *args, **kwargs):
        return super(ProductViewset, self).retrieve(self, request, *args, **kwargs)


class SoldProductsListView(ListAPIView):
    queryset = SoldProducts.objects.filter(is_done=True)
    serializer_class = SoldProductsSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = [AllowAny]
    lookup_field = ['product.code']
    parser_classes = (JSONParser,)
    pagination_class = SoldProductPagination

    @swagger_auto_schema(operation_summary="Sotilgan mahsulotlar haqidagi malumotlar ro'yhatini chop etish")
    def get(self, request, *args, **kwargs):
        return super(SoldProductsListView, self).get(self, request, *args, **kwargs)


class SoldProductView(CreateAPIView):
    queryset = SoldProducts.objects.all()
    serializer_class = SoldProductsSerializer
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Mahsulotni sotish")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SoldProductCreateView(GenericAPIView):
    queryset = SoldProducts.objects.all()
    serializer_class = SoldProductsSerializer

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mahsulot sotish")
    def post(self, request, *args, **kwargs):
        try:
            product_code = request.data.get("product_code").lower()
            product = Product.objects.filter(code__icontains=product_code).first()
            sold_product = self.get_queryset().filter(product=product, is_done=False).first()
            if sold_product:
                sold_product.buy_count += 1
                sold_product.save()
                return Response(data=
                                {
                                 "name": sold_product.product.name,
                                 "buy_count": sold_product.buy_count,
                                 "price": sold_product.product.selling_price * sold_product.buy_count
                                 }, status=status.HTTP_200_OK)
            else:
                queryset = SoldProducts(product=product)
                queryset.save()
                serializer = self.get_serializer(queryset)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response(data={"message": "Product not found"}, status=status.HTTP_200_OK)


class SoldProductDoneView(GenericAPIView):
    queryset = SoldProducts.objects.all()
    serializer_class = SoldProductsSerializer

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mahsulot sotishni yakunlash")
    def post(self, request, *args, **kwargs):
        try:
            product_code = request.data.get("product_code").lower()
            product = Product.objects.filter(code__icontains=product_code).first()
            sold_product = SoldProducts.objects.filter(product=product, is_done=False).first()
            if sold_product:
                sold_product.is_done = True
                sold_product.save()
                serializer = self.get_serializer(instance=sold_product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(data={"message": "Product not found"}, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(data={"message": "Product not found or something is wrong"}, status=status.HTTP_200_OK)


class NetProfit(GenericAPIView):
    queryset = SoldProducts.objects.filter(is_done=True)
    serializer_class = SoldProductsSerializer
    parser_classes = [JSONParser, ]

    @swagger_auto_schema(operation_summary='Sof foydalar royhatini chop etish royhatini chop etish')
    def get(self, request, *args, **kwargs):
        my_dict = defaultdict(float)
        for obj in self.get_queryset():
            try:
                my_dict[obj.product.name] += (obj.buy_count *
                                              (obj.product.selling_price - obj.product.original_price))
            except Exception as exc:
                pass
        return Response(data=my_dict, status=status.HTTP_200_OK)


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = [AllowAny, ]
    # permission_classes = [IsAdminUser, ]
    parser_classes = [JSONParser, ]

    @swagger_auto_schema(operation_summary='Kategoriyalar royhatini chop etish')
    def list(self, request, *args, **kwargs):
        return super(CategoryViewset, self).list(self, request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Yangi Kategoriya qo'shish")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Kategoriya malumotlarini yangilash")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Kategoriya malumotlarini qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Kategoriya malumotlarini o'chirish")
    def destroy(self, request, *args, **kwargs):
        return super(CategoryViewset, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Kategoriya haqidagi malumotlarini chop etish (retrieve)")
    def retrieve(self, request, *args, **kwargs):
        return super(CategoryViewset, self).retrieve(self, request, *args, **kwargs)
