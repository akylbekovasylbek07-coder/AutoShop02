from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.cart.models import CartItem
from apps.cart.utils import get_cart
from apps.product.models import Product


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=product,
            defaults={'price': product.price},
        )
        if not created:
            item.quantitly += 1
            item.save(update_fields=['quantitly'])

        return redirect(request.META.get('HTTP_REFERER', '/'))


class CartDeleteView(TemplateView):
    template_name = 'pages/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        return context


class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
