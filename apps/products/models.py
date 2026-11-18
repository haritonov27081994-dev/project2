from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL-метка (slug)")

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'
        ordering = ['name']

    def __str__(self):
        return self.name


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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Категория",
        null=True,
        blank=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Производитель",
        null=True,
        blank=True
    )
    viewed_by_users = models.ManyToManyField(
        User,
        related_name='viewed_products',
        blank=True,
        verbose_name="Просмотрено пользователями"
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_products',
        blank=True,
        verbose_name="В избранном у пользователей"
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
