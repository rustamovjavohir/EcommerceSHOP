import random
from collections import defaultdict

from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 110


class SoldProductPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 120


def netProfit(objects):
    my_dict = defaultdict(float)
    for obj in objects:
        try:
            my_dict[obj.product.name] += (obj.buy_count *
                                          (obj.product.selling_price - obj.product.original_price))
        except Exception as exc:
            pass
