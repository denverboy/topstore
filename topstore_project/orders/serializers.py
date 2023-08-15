import datetime

from rest_framework import serializers

from orders.models import Order, OrderItems
from products.serializers import ImagesProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.id')
    price = serializers.ReadOnlyField(source='product.price')
    free_delivery = serializers.ReadOnlyField(source='product.free_delivery')
    images = ImagesProductSerializer(source='product.images', many=True)
    quantity = serializers.ReadOnlyField()

    class Meta:
        model = OrderItems
        fields = [
            'id',
            'title',
            'category',
            'price',
            'quantity',
            'free_delivery',
            'images'
        ]


class OrderSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='user.profile.full_name')
    email = serializers.ReadOnlyField(source='user.profile.email')
    phone = serializers.ReadOnlyField(source='user.profile.phone')
    items = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'free_delivery',
            'payment_type',
            'total_cost',
            'status',
            'full_name',
            'city',
            'address',
            'email',
            'phone',
            'items'
        ]


class OrderConfirmSerializer(serializers.Serializer):
    city = serializers.CharField()
    address = serializers.CharField()
    PAYMENT_METHOD = [
        ('online', 'online'),
        ('offline', 'offline')
    ]
    payment_type = serializers.ChoiceField(choices=PAYMENT_METHOD)
    phone = serializers.CharField(required=False)


class PaymentSerializer(serializers.Serializer):
    number = serializers.CharField()
    name = serializers.CharField()
    month = serializers.CharField()
    year = serializers.CharField()
    code = serializers.CharField()

    def validate_number(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError(
                "The card number must be only 16 digits."
            )
        return value

    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("The name must not contain numbers")
        return value

    def validate_month(self, value):
        if not value.isdigit() or not (1 <= int(value) <= 12):
            raise serializers.ValidationError("Invalid month")
        return value

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if not value.isdigit() or int(value) + 2000 < current_year:
            raise serializers.ValidationError("Card expired")
        return value

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 3:
            raise serializers.ValidationError(
                "CVV number must contain only 3 digits"
            )

    def validate(self, data):
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        if int(data['year']) + 2000 < current_year or (
                int(data['year']) + 200 == current_year and int(data['month']) < current_month):
            raise serializers.ValidationError("Card expired")
        return data
