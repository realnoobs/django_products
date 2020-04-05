from django.conf.urls import url, include
from django.urls import path

from . import views

app_name = 'django_products'

urlpatterns = (
    path('tag/<str:tag>/', views.TaggedProductsView.as_view(), name="tag"),
    path('category/<str:category>/', views.CategorizedProductsView.as_view(), name="category"),
)