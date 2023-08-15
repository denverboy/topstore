from rest_framework import serializers

from products.models import Product
from products.serializers import ImagesProductSerializer


class BasketSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    price = serializers.ReadOnlyField(source='product.price')
    images = ImagesProductSerializer(source='product.images', many=True)
    quantity = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'images',
            'quantity'
        ]


class RemoveProductsBasketSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    count = serializers.IntegerField(min_value=1)


class AddProductsBasketSerializer(RemoveProductsBasketSerializer, serializers.Serializer):

    def validate(self, data):
        """
        We have to assume that the quantity is not too affordable quantity of the product.
        """
        if 'id' in data and 'count' in data:
            product = data['id']
            count = data['count']
            if product.count < count:
                raise serializers.ValidationError({
                    'count': ['Not enough product in stock.']
                })
        return data
