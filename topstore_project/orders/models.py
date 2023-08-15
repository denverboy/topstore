from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.PROTECT
    )
    products = models.ManyToManyField(Product, through='OrderItems', blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    free_delivery = models.BooleanField(default=False)
    PAYMENT_METHOD = [
        ('online', 'online'),
        ('offline', 'offline')
    ]
    payment_type = models.CharField(
        max_length=7, choices=PAYMENT_METHOD, blank=True
    )
    status = models.BooleanField(default=False)


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    quantity = models.PositiveSmallIntegerField(default=0)
