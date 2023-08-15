from django.db.models import Sum, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.filters import CatalogFilter
from catalog.models import Category, Tag
from catalog.serializers import CategorySerializer, TagSerializer, ProductForCatalogSerializer
from orders.models import OrderItems
from products.models import Product


class CategoriesAPIView(APIView):
    @extend_schema(
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        """Get catalog menu"""

        subcategories_id = list()
        categories = Category.objects.all()

        for sub_c in categories:
            if sub_c.subcategories is not None:
                subcategories_id.append(sub_c.subcategories.id)

        categories = categories.exclude(id__in=subcategories_id)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class CatalogListAPIView(ListAPIView):
    """Get catalog items"""

    serializer_class = ProductForCatalogSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = [
        'title',
        'description'
    ]
    filterset_class = CatalogFilter
    ordering_fields = [
        'price',
        'rating',
        'reviews',
        'date'
    ]

    def get_queryset(self):
        return Product.objects.annotate(
            reviews_count=Count('reviews'),
            rating_annotate=Avg('reviews__rate'),
        ).all()


class ProductsLimitListAPIView(ListAPIView):
    """Get catalog limeted items"""

    queryset = Product.objects.filter(count__lt=10)
    serializer_class = ProductForCatalogSerializer


class ProductPopularListAPIView(ListAPIView):
    """Get catalog popular items"""

    serializer_class = ProductForCatalogSerializer

    def get_queryset(self):
        products = (
            OrderItems.objects
            .values('product')
            .annotate(total=Sum('quantity'))
            .order_by('-total')
        )
        popular_products = products[:3]
        top_products_id = [item['product'] for item in popular_products]
        return Product.objects.filter(id__in=top_products_id)


class BannersListAPIView(ListAPIView):
    """Get banner items"""

    queryset = Product.objects.all()
    serializer_class = ProductForCatalogSerializer


class TagsAPIView(APIView):
    @extend_schema(
        responses={200: TagSerializer(many=True)}
    )
    def get(self, request):
        """Get tags"""

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
