from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Продавец",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        verbose_name="Изображение товара",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус модерации"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
