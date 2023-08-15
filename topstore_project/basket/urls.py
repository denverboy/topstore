from django.urls import path

from basket.views import BasketAPIView

app_name = 'basket'


urlpatterns = [
    path('basket/', BasketAPIView.as_view(), name='basket')
]
