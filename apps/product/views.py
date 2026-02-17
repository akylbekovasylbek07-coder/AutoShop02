from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_list_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Prefetch

from apps.product.models import (
    Category, Product,
    ProductVariant, Review)

class CategoryListView(ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent__isnull=True)

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True
        )[:6]
        context['product'] = Product.objects.filter(
            is_available=True, 
            category__is_active=True 
        )[:8]
        return context