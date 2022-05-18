from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class TestProduct(APITestCase):

    def setUp(self):
        self.list_url = reverse('product-list')
        self.category = Category.objects.create(name='category1')
        self.data = {
            "name": "product1",
            "category_id": self.category.id,
            "product_count": 5,
            "original_price": 10000.0,
            "selling_price": 20500.0,
            "code": "code",
            "is_delete": False
        }

        self.update_data = {
            "name": "product2"
        }

    def test_list(self):
        # print(resolve(self.url))
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # import pdb
        # pdb.set_trace()

    def test_create_product(self):
        response = self.client.post(self.list_url, data=self.data, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'product1')
        # self.assertDictEqual(response.data, self.data)

    def test_update_product(self):
        product = Product.objects.create(name='product1', category_id=self.category, product_count=5,
                                         original_price=10000.0, selling_price=20500.0, code='code', is_delete=False)
        response = self.client.patch(reverse('product-detail', kwargs={'pk': product.id}),
                                     data=self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'product2')

    def test_delete_product(self):
        product = Product.objects.create(name='product1', category_id=self.category, product_count=5,
                                         original_price=10000.0, selling_price=20500.0, code='code', is_delete=False)
        response = self.client.delete(reverse('product-detail', kwargs={'pk': product.id}),
                                      data=self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(Product.objects.count(), 0)
        # self.assertIsNone(Product.objects.filter(id=product.id).first())
