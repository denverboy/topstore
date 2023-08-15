from rest_framework import serializers

from catalog.models import Category, Tag
from products.models import Review, Product
from products.serializers import ImagesProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'image',
            'subcategories'
        ]

    def get_subcategories(self, obj):
        """Serialize subcategories"""
        subcategories = Category.objects.get(id=obj.id).subcategories

        if subcategories:
            return CategorySerializer(subcategories).data
        return []


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductForCatalogSerializer(serializers.ModelSerializer):
    images = ImagesProductSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'free_delivery',
            'images',
            'tags',
            'reviews',
            'rating'
        )

    def get_reviews(self, obj):
        return Review.objects.filter(product=obj).count()
