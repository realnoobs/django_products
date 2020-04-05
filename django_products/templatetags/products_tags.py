from django.template import Library
from django.template.loader import get_template
from django_products.models import Category

register = Library()

@register.simple_tag
def product_template(product):
    context = {'product': product}
    opts = product.get_real_instance_class()._meta
    template = get_template('%s/%s_product.html' % (opts.app_label, opts.model_name))
    return template.render(context=context)
