from django.db import models

# Create your models here.
from django_products.models import Product
from django_products.mixins import InventoryMixin


class Book(InventoryMixin, Product):
    class Meta:
        verbose_name = 'Book'


class Video(InventoryMixin, Product):
    class Meta:
        verbose_name = 'Video'


class Music(InventoryMixin, Product):
    class Meta:
        verbose_name = 'Music'
