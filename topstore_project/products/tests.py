from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product, Review
from products.serializers import ProductSerializer


class ProductsTestCase(APITestCase):
    fixtures = [
        'custom_auth/fixtures/users-fixtures.json',
        'custom_auth/fixtures/profiles-fixtures.json',
        'catalog/fixtures/catalog-fixtures.json',
        'products-fixtures.json',
    ]

    def setUp(self) -> None:
        self.product = Product.objects.get(pk=1)
        self.user = User.objects.get(pk=1)

    def test_get_product_detail(self):
        url = reverse('products_api:product_details', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ProductSerializer(self.product).data

        self.assertEqual(response.data, expected_data)

    def test_create_review(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('products_api:review_create', args=[self.product.pk])
        data = {
            "text": "I love this phone!",
            "rate": 5,
            'user': self.user,
            'product': self.product

        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        review = Review.objects.filter(text=data['text']).first()
        self.assertEqual(review.text, data['text'])
        self.assertEqual(review.rate, data['rate'])
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
