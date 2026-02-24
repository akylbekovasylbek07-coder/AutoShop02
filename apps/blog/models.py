from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    tags = models.ManyToManyField(Tag, related_name="posts")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    img = models.ImageField(upload_to="posts/", verbose_name="Изображение")
    desc = CKEditor5Field("Описание", config_name="extends")
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
