from django.urls import path

from orders.views import OrderAPIView, OrderDetailAPIVIew, PaymentAPIView

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderAPIView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailAPIVIew.as_view(), name='confirm-order'),
    path('order/<int:pk>/payment/', PaymentAPIView.as_view(), name='payment')
]
