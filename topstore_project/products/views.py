from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, Review
from products.serializers import ProductSerializer, ReviewsSerializer


class ProductAPIView(APIView):
    @extend_schema(
        responses={200: ProductSerializer}
    )
    def get(self, request, pk):
        """Get product detail"""

        product = get_object_or_404(Product, pk=pk)
        serialized = ProductSerializer(product)
        return Response(serialized.data)


class ReviewAPIView(CreateAPIView):
    """Create review for product"""

    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, product=product)
