from .api import urlpatterns as api_urls
from django.urls import path
from .views import *

urlpatterns = [
    path("soldproductlist/", SoldProductsListView.as_view(), name="soldproductlist"),
    path("soldproductcreate/", SoldProductCreateView.as_view(), name="soldproductcreate"),
    path("soldproductdone/", SoldProductDoneView.as_view(), name="soldproductdone"),
    path("soldproduct/", SoldProductView.as_view(), name="soldproduct"),
    path("netprofit/", NetProfit.as_view(), name="netprofit"),
]

urlpatterns += api_urls
