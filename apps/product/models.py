from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brand/', null=True, blank=True)

    def _str_(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество товара на складе")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE , related_name='images'
    )
    image = models.ImageField(upload_to='iproduct/')
    # is_main - models.BooleanField(default=False, verbose_name="Главная картинка")

    def _str_(self):
        return self.product.name
    
class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name
    
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    def _str_(self):
        return self.name
    

class ProductVariant( models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    attribute = models.ManyToManyField(AttributeValue)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    sku = models.CharField(max_length=255, unique=True, verbose_name="Артикул")

    def _str_(self):
        return f"{self.product.name} {self.sku}"
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.product.name} {self.rating}"