from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

from catalog.models import Category, Tag


def product_img_directory_path(instance, filename):
    return f'products/product-{instance.product.pk}/{filename}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    full_description = models.TextField(blank=True)
    free_delivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def rating(self):
        average_rating = self.reviews.aggregate(average_rating=Avg('rate'))['average_rating']
        return average_rating if average_rating is not None else 0

    def __str__(self):
        return f'{self.title}'


class ImagesProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to=product_img_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.CharField(blank=True, max_length=1000)
    RATE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rate = models.IntegerField(choices=RATE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user id: {self.user.pk} about product id: {self.product.pk}'


class SpecificationName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class SpecificationValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.value}'


class Specifications(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications')
    name = models.ForeignKey(SpecificationName, on_delete=models.CASCADE)
    value = models.ForeignKey(SpecificationValue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product id: {self.product.pk} | specifications # {self.pk}'
