from django.db import models


class ContactPage(models.Model):
    map  = models.TextField(verbose_name= "Карта")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    desc = models.TextField(verbose_name="Описание")
    address = models.TextField( max_length=255, verbose_name="Адрес")
    email = models.EmailField( verbose_name="Email")
    phone = models.CharField(max_length=30, verbose_name="Телефон")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class ContactRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=100, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Заявки на сайте"
        verbose_name_plural = "Заявки на сайте"        



