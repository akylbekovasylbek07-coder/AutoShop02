from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.abuot.models import Slider
from apps.partners.models import Partners
from apps.product.models import Category, Product, WislistItem
from apps.product.utils import get_wislist


class WislistView(TemplateView):
    template_name = 'pages/wislist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist'] = get_wislist(self.request)
        return context


class ToggleWislistView(View):
    def post(self, request, product_id):
        wislist = get_wislist(request)
        product = get_object_or_404(Product, id=product_id)
        item = WislistItem.objects.filter(
            wislist=wislist,
            product=product,
        ).first()

        if item:
            item.delete()
        else:
            WislistItem.objects.create(
                wislist=wislist,
                product=product,
            )
        return redirect(request.META.get('HTTP_REFERER', '/'))


class SearchView(TemplateView):
    template_name = 'pages/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Product.objects.none()

        return Product.objects.filter(
            Q(name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(car_models__brand__name__icontains=query)
        ).distinct().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        context['products'] = self.get_queryset()
        return context


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True,
            parent__isnull=True,
        )[:6]
        context['products'] = Product.objects.filter(
            is_available=True,
            category__is_active=True,
        ).prefetch_related('images')[:8]
        context['partners'] = Partners.objects.all()
        context['sliders'] = Slider.objects.filter(is_active=True).order_by(
            'order',
            '-created_at',
        )
        return context


class CategoryDetailView(TemplateView):
    template_name = 'pages/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.filter(is_active=True),
            slug=self.kwargs['slug'],
        )
        context['category'] = category
        context['products'] = Product.objects.filter(
            is_available=True,
            category=category,
        ).prefetch_related('images')
        return context


class LegacyHtmlRedirectView(View):
    route_map = {
        'index': 'home',
        'shop': 'home',
        'shop-fullwidth': 'home',
        'shop-fullwidth-list': 'home',
        'shop-right-sidebar': 'home',
        'shop-right-sidebar-list': 'home',
        'shop-list': 'home',
        'product-details': 'home',
        'product-sidebar': 'home',
        'product-grouped': 'home',
        'variable-product': 'home',
        'product-countdown': 'home',
        'about': 'about',
        'contact': 'contact',
        'cart': 'cart_detail',
        'wishlist': 'wishlist',
        'login': 'login',
        'my-account': 'profile',
        'checkout': 'cart_detail',
        'blog': 'blog_page',
        'blog-details': 'blog_page',
        'blog-fullwidth': 'blog_page',
        'blog-sidebar': 'blog_page',
        'blog-no-sidebar': 'blog_page',
        'compare': 'home',
        'privacy-policy': 'home',
        'coming-soon': 'home',
        'faq': 'home',
        '404': 'home',
    }

    def get(self, request, legacy_page):
        return redirect(self.route_map.get(legacy_page, 'home'))
