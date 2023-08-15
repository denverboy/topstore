from django.urls import path

from catalog.views import (
    CategoriesAPIView,
    TagsAPIView,
    BannersListAPIView,
    ProductsLimitListAPIView,
    CatalogListAPIView, ProductPopularListAPIView
)

app_name = 'catalog'

urlpatterns = [
    path('category/', CategoriesAPIView.as_view(), name='category'),
    path('catalog/', CatalogListAPIView.as_view(), name='catalog'),
    path('products-limit/', ProductsLimitListAPIView.as_view(), name='product-limit'),
    path('products-popular/', ProductPopularListAPIView.as_view(), name='products-popular'),
    path('tags/', TagsAPIView.as_view(), name='tags'),
    path('banners/', BannersListAPIView.as_view(), name='banners'),
]