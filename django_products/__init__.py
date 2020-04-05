default_app_config = 'django_products.apps.DjangoProductsConfig'


def get_product_model():
    from django.core.exceptions import ImproperlyConfigured
    from django.conf import settings
    from django.apps import apps

    if not apps.is_installed('django_products'):
        raise Exception(
            "Product model fail to load, "
            "may be django_products app is not installed,"
            "Please add django_product to INSTALLED_APPS settings"
        )

    # TODO implement swappable model for product
    PRODUCT_MODEL = getattr(settings, 'PRODUCT_MODEL', 'django_products.Product')

    try:
        return apps.get_model(PRODUCT_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PRODUCT_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "PRODUCT_MODEL refers to model '%s' that has not been installed" % settings.PRODUCT_MODEL
        )
