from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q, UniqueConstraint

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="название катерогии")
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True, verbose_name="Родитель"
    )
    is_active = models.BooleanField(default=True, verbose_name='Активация')

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

    

class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название бренды")
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brand/',verbose_name="Лого бренда", null=True, blank=True)

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)   
    
    
    class Meta:
        verbose_name_plural = 'Бренды'
        verbose_name = 'бренды'

class CarModel(models.Model):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE,
        related_name='models', verbose_name="Бренд" 
    )    
    name = models.CharField(max_length=150, verbose_name="Название модели")
    generation = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Поколение"
    )
    year_from = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска", blank=True, null=True
    )

    def __str__(self):
        return f"{self.brand.name} {self.name} {self.generation or ''}"

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        related_name='products'
    )
    car_models = models.ManyToManyField(
        CarModel, related_name='products', verbose_name="модель авто"
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

    def get_main_image(self):
        return self.images.filter(is_main=True).first()
    
    def get_second_image(self):
        return self.images.filter(is_main=False).first()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Продукт'
        verbose_name = 'продукт'

    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='product/', verbose_name="Фото")
    
    # 1. Бул жерди активдештирдик:
    is_main = models.BooleanField(default=False, verbose_name="Главная картинка")

    def __str__(self):
        return f"Фото для {self.product.name}"
    
    def save(self, *args, **kwargs):
        # 2. Эгер бул сүрөт негизги болсо, калгандарын "негизги эмес" кылабыз
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        
        # super() методун if'дин сыртына чыгардык, ошондо бардык сүрөттөр сакталат
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Фото товара'
        verbose_name = 'фотка товара'
        constraints = [
            UniqueConstraint(
                fields=['product'],
                condition=Q(is_main=True),
                name='unique_main_image_per_product'
            )
        ]
    
class Attribute(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name="Категория", null=True, blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Атрибут'
        verbose_name = 'атрибут'

    
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values', verbose_name='Название')
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name_plural = 'Значение атрибута'
        verbose_name = 'значение атрибута'

    

class ProductVariant( models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Название')
    # Мындай болушу керек:
    attributes = models.ManyToManyField(AttributeValue, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.PositiveIntegerField(default=1, verbose_name="Название товара на складе")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Артикул")

    def __str__(self):
        return f"{self.product.name} {self.sku}"
    
    class Meta:
        verbose_name_plural = 'Вариант продукта'
        verbose_name = 'вариант продукта'

    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} {self.rating}"
    
    class Meta:
        verbose_name_plural = 'Oтзывы'
        verbose_name = 'отзывы'


class Slider(models.Model):
    title = models.CharField(max_length=80, verbose_name="Заголовок")
    image = models.ImageField(upload_to='slider/', null=True, verbose_name="Фото")
    small_text = models.TextField(verbose_name="Краткое описание")
    name_button = models.CharField(max_length=80, verbose_name="Название кнопки")
    link_button = models.URLField(max_length=255, verbose_name="Ссылка кнопки")

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = 'Слайдер'
        verbose_name = 'слайдер'

class Wislist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True, 
        blank=True, related_name='wislist'
        )
    session_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Избранное {self.id}"
    
    def total_items(self):
        return self.items.count()


class WislistItem(models.Model):
    wislist = models.ForeignKey(Wislist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('wislist', 'product')

