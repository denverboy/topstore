from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='BasketItems', blank=True)


class BasketItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_items')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
