from django.contrib import admin
from django.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django_products.models import Product, Category, Tag, TaggedProduct

from mptt.admin import MPTTModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    pass


@admin.register(TaggedProduct)
class TaggedProductAdmin(admin.ModelAdmin):
    list_display = ['tag', 'content_object']


class ProductChildAdmin(PolymorphicChildModelAdmin):
    base_model = Product


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    """ Parent admin Product Model, set child model in settings """

    def get_child_models(self):

        child_models_list = getattr(settings, 'PRODUCT_CHILD_MODELS', None)

        if not child_models_list:
            raise NotImplementedError("Implement PRODUCT_CHILD_MODELS in settings")

        try:
            models = [apps.get_model(child_models, require_ready=True) for child_models in child_models_list]
            return models
        except ValueError:
            raise ImproperlyConfigured("PRODUCT_CHILD_MODELS item must be of the form 'app_label.model_name'")
        except LookupError:
            raise ImproperlyConfigured(
                "Make sure all of PRODUCT_CHILD_MODELS is installed"
            )
