from django.contrib import admin

# Register your models here.
from django_products.models import Product
from django_products.admin import ProductChildAdmin

from .models import Book, Video, Music


@admin.register(Book)
class BookAdmin(ProductChildAdmin):
    base_model = Product


@admin.register(Video)
class VideoAdmin(ProductChildAdmin):
    base_model = Product


@admin.register(Music)
class MusicAdmin(ProductChildAdmin):
    base_model = Product
