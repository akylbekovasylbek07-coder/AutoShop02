from django.db import models


class Partners(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    link = models.URLField(
        max_length=255,
        verbose_name="Ссылка",
        help_text="Ссылка на сайт или инстаграм или что-то еще",
    )
    logo = models.ImageField(upload_to="partners/", verbose_name="Логотип")

    def __str__(self):
        return f"{self.title} {self.link}"

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
