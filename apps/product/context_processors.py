from apps.cart.utils import get_cart
from apps.product.models import Brand, Category
from apps.product.utils import get_wislist


def shop_layout_context(request):
    return {
        'categories': Category.objects.filter(
            is_active=True,
            parent__isnull=True,
        )[:12],
        'brands': Brand.objects.all()[:20],
        'wishlist': get_wislist(request),
        'cart': get_cart(request),
    }
