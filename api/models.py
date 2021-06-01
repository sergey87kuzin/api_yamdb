from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
        null=False,
        db_index=True,
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    genres = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр'
    )

    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name, self.genres, self.category


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
