from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import ProductVariant


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True, null=True
    )
created_at  = models.DateField(auto_now_add=True)
 
def _str_ (self):
    return f"корзина: {self.id}"

class CartItem (models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    varant = models.ForeignKey(ProductVariant, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

     
def _str_ (self):
    return self.variant.product.name

@property
def total_price(self):
    return self.variant.price * self.quantitly
