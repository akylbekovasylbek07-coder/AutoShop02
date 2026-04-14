from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import get_list_or_404, redirect


from apps.cart.models import CartItem
from apps.product.models import Product
from apps.cart.utils import get_cart


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_list_or_404(Product, id=product_id)
        cart = get_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price':product.price},
        )
        if not created:
            item.quantitly+=1
            item.save()

        return redirect(redirect.META.get('HTTP_REFERER', '/'))    
    
class CartDeleteView(View):
    temlate_name = 'pages/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.cart = get_cart(self.request)
        return self.cart.items.select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart(self.request)
        return context

class RemoveFromCartView(DetailView):
    model = CartItem

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER,' '/') 