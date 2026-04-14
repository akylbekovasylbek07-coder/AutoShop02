from django.db import models
from django.conf import settings
from apps.product.models import Product


User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True, null=True, related_name='carts'
    )
    session_key = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_quantity(self):
        return sum(item.quantitly() for item in self.items.all())

    def __str__(self):
        return f"корзина: {self.id}"
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantitly = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} {self.quantitly}"

  
    def total_price(self):
        return self.price * self.quantitly
    
    class Meta:
        unique_together = ('cart', 'variant')
