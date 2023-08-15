import time

from celery import shared_task
from django.db.models import F

from orders.models import Order
from products.models import Product


@shared_task
def reserve_products_from_stock(items):
    for product_id, quantity in items:
        Product.objects.filter(id=product_id).update(count=F('count') - quantity)


@shared_task
def check_status_order(order_id, items):
    order = Order.objects.get(id=order_id)
    if not order.status:
        for product_id, quantity in items:
            Product.objects.filter(id=product_id).update(count=F('count') + quantity)


@shared_task
def check_status_payment(order_id):
    time.sleep(60)

    order = Order.objects.get(pk=order_id)
    order.status = True
    order.save()
