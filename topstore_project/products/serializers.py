from rest_framework import serializers

from products.models import ImagesProduct, Review, Specifications, Product


class ImagesProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesProduct
        fields = 'image', 'description'


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = (
            'author', 'email', 'text', 'rate', 'date'
        )

    def get_author(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'


class SpecificationsSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.name')
    value = serializers.ReadOnlyField(source='value.value')

    class Meta:
        model = Specifications
        fields = ('name', 'value')


class ProductSerializer(serializers.ModelSerializer):
    images = ImagesProductSerializer(many=True)
    tags = serializers.StringRelatedField(many=True)
    reviews = ReviewsSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'pk',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'full_description',
            'free_delivery',

            'images',
            'tags',
            'reviews',
            'specifications',
            'rating'
        )
