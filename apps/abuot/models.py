from django.db import models

class AboutContent(models.Model):
    big_img = models.ImageField(upload_to="about/", verbose_name="Большое изображение")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    desc = models.TextField(verbose_name="Описание")
    autograph_img = models.ImageField(upload_to="about/", verbose_name="Авторская фотография")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class PlusAbout(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    desc = models.TextField(verbose_name="Описание")
    img = models.ImageField(upload_to="about/", verbose_name="Изображение")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Плюсы"
        verbose_name_plural = "Плюсы"



class BlogAbout(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    desc = models.TextField(verbose_name="Описание")
    img = models.ImageField(upload_to="about/", verbose_name="Изображение")


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блог"


class Fag(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    desc = models.TextField(verbose_name="Описание")
   
    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = "Вопросы/Ответы"
        verbose_name_plural = "вопросы/ответы"



class Testimonials(models.Model):
    avatar = models.ImageField(upload_to="about/", verbose_name="Аватар")
    name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")
    desc = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "отзывы"
        verbose_name_plural = "отзывы "



class Slider(models.Model):
    ALIGN_CHOICES = (
        ("left", "Слева"),
        ("center", "По центру"),
    )

    title = models.CharField(max_length=150, verbose_name="Заголовок")
    subtitle = models.CharField(
        max_length=150, blank=True, verbose_name="Подзаголовок"
    )
    description = models.CharField(
        max_length=255, blank=True, verbose_name="Описание"
    )
    button_text = models.CharField(
        max_length=50, blank=True, verbose_name="Текст кнопки"
    )
    button_link = models.URLField(
        max_length=255, blank=True, verbose_name="Ссылка кнопки"
    )
    image = models.ImageField(upload_to="slider/", verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    text_align = models.CharField(
        max_length=10,
        choices=ALIGN_CHOICES,
        default="left",
        verbose_name="Выравнивание",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"

    def __str__(self):
        return self.title
