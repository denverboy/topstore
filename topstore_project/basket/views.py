from django.contrib.auth.mixins import LoginRequiredMixin
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import Basket, BasketItems
from basket.serializers import (
    AddProductsBasketSerializer,
    BasketSerializer,
    RemoveProductsBasketSerializer
)


class BasketAPIView(LoginRequiredMixin, APIView):
    """Get items in basket"""

    @extend_schema(
        responses={200: BasketSerializer(many=True)}
    )
    def get(self, request):
        user = request.user

        basket = Basket.objects.get(user_id=user.id)
        basket_items = BasketItems.objects.filter(basket=basket)
        serializer = BasketSerializer(basket_items, many=True)

        if len(serializer.data) == 0:
            return Response(
                {"message": "Basked is empty"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={201: AddProductsBasketSerializer}
    )
    def post(self, request):
        serializer = AddProductsBasketSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get('id')
            count = serializer.validated_data.get('count')
            user = request.user

            basket, created = Basket.objects.get_or_create(user=user)
            basket_item, create = BasketItems.objects.get_or_create(
                basket=basket,
                product=product
            )
            if create:
                basket_item.quantity = count
            else:
                basket_item.quantity += count
            basket_item.save()

            return Response({"message": "Product added to basket"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        responses={200: RemoveProductsBasketSerializer}
    )
    def patch(self, request):
        """Update product quantity"""

        serializer = RemoveProductsBasketSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get('id')
            count = serializer.validated_data.get('count')
            user = request.user

            basket = Basket.objects.get(user=user)
            try:
                basket_item = BasketItems.objects.get(
                    basket=basket,
                    product=product
                )
            except BasketItems.DoesNotExist:
                return Response(
                    {'error': 'Product not found in the basket'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if basket_item.quantity <= count:
                basket_item.delete()
            else:
                basket_item.quantity -= serializer.validated_data.get('count')
                basket_item.save()
            return Response(
                {'message': 'Product quantity updated'},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        """Delete all items in basket"""

        user = request.user
        basket = Basket.objects.get(user=user)
        BasketItems.objects.filter(basket=basket).delete()

        return Response(
            {'message': 'Basket is empty'},
            status=status.HTTP_200_OK
        )
