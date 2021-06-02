from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
        blank=True,
        db_index=True,
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='Описание',
    )
    genres = models.ManyToManyField(
        'Genre',
        blank=True,
        verbose_name='Жанр',
        related_name='titles',
    )

    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug'
    )

    def __str__(self):
        return self.name
