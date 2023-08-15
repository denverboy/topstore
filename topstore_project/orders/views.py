from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import BasketItems
from orders.models import Order, OrderItems
from orders.serializers import OrderSerializer, OrderConfirmSerializer, PaymentSerializer

from .tasks import reserve_products_from_stock, check_status_order, check_status_payment


class OrderAPIView(LoginRequiredMixin, APIView):
    def post(self, request):
        """Create order"""

        user = request.user

        items = BasketItems.objects.filter(basket__user=user).select_related('product')
        total_cost = items.aggregate(total=Sum(F('quantity') * F('product__price')))['total']

        order = Order.objects.create(
            user=user,
            total_cost=total_cost
        )
        free_delivery = True
        order_items_data = list()
        items_data_for_celery = list()

        for item in items:
            order_items_data.append(OrderItems(order=order, product=item.product, quantity=item.quantity))
            items_data_for_celery.append((item.product.id, item.quantity))
            if not item.product.free_delivery:
                free_delivery = False

        order.free_delivery = free_delivery
        order.save()

        OrderItems.objects.bulk_create(order_items_data)

        items.delete()

        reserve_products_from_stock.delay(items_data_for_celery)

        check_status_order.apply_async((order.id, items_data_for_celery), countdown=2*60)

        return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        """Get user orders"""

        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OrderDetailAPIVIew(LoginRequiredMixin, APIView):
    @extend_schema(
        responses={200: OrderSerializer}
    )
    def get(self, request, pk):
        """Get order detail"""
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        responses={200: OrderConfirmSerializer}
    )
    def post(self, request, pk):
        """Confirm order"""

        order = get_object_or_404(Order, pk=pk)
        serializer = OrderConfirmSerializer(data=request.data)
        if serializer.is_valid():
            order.city = serializer.validated_data.get('city')
            order.address = serializer.validated_data.get('address')
            order.payment_type = serializer.validated_data.get('payment_type')

            order.phone = serializer.validated_data.get('phone', order.phone)

            order.save()
            return Response(
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentAPIView(LoginRequiredMixin, APIView):
    @extend_schema(
        responses={200: PaymentSerializer}
    )
    def post(self, request, pk):
        """Payment system simulator"""

        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            # Имитируем задержку ответа из банка
            check_status_payment.delay(order_id=pk)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
