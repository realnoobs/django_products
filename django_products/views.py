from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from django_products.models import Product, Tag, Category


class TaggedProductsView(TemplateView):
    model = Tag
    template_name = 'products/tag_page.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('tag')
        tag = get_object_or_404(self.model, slug=slug)
        context = {
            'tag': tag,
            'tagged_products': tag.tagged_products.all()
        }
        kwargs.update(**context)
        return super().get_context_data(**kwargs)


class CategorizedProductsView(TemplateView):
    model = Category
    template_name = 'products/category_page.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('category')
        category = get_object_or_404(self.model, slug=slug)
        context = {
            'category': category,
            'products': category.products.all()
        }
        kwargs.update(**context)
        return super().get_context_data(**kwargs)


class ProductIndexView(ListView):
    model = Product
    template_name = 'products/product_index.html'


class ProductDetailView(TemplateView):
    model = Product
    template_name = 'products/product_page.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('product')
        product = get_object_or_404(self.model, slug=slug)
        context = {
            'product': product
        }
        kwargs.update(**context)
        return super().get_context_data(**kwargs)
