from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="название катерогии")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Активация')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

    

class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название бренды")
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brand/',verbose_name="Лого бренда", null=True, blank=True)

    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Бренды'
        verbose_name = 'бренды'

    

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='Название'
    )
    name = models.CharField(max_length=150, verbose_name=" Название товара")
    slug = models.SlugField(unique=True)
    description = models.TextField( verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество товара на складе")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Продукт'
        verbose_name = 'продукт'

    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='product/', verbose_name="Фото")
    #is_main - models.BooleanField(default=False, verbose_name="Главная картинка")

    def _str_(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Фото'
        verbose_name = 'фотки'

    
class Attribute(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)

    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Атрибут'
        verbose_name = 'атрибут'

    
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values', verbose_name='Название')
    value = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.attribute.name} {self.value}"
    
    class Meta:
        verbose_name_plural = 'Значение атрибута'
        verbose_name = 'значение атрибута'

    

class ProductVariant( models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Название')
    attributes = models.ManyToManyField(AttributeValue)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1, verbose_name="НАзвание товара на складе")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Артикул")

    def _str_(self):
        return f"{self.product.name} {self.sku}"
    
    class Meta:
        verbose_name_plural = 'Вариант продукта'
        verbose_name = 'вариант продукта'

    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.product.name} {self.rating}"
    
    class Meta:
        verbose_name_plural = 'Oтзывы'
        verbose_name = 'отзывы'
