from django.urls import path

from products.views import ProductAPIView, ReviewAPIView

app_name = 'products'


urlpatterns = [
    path('product/<int:pk>/', ProductAPIView.as_view(), name='product'),
    path('product/<int:pk>/reviews/', ReviewAPIView.as_view(), name='reviews')
]
