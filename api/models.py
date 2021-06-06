from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email, **extra_fields):
        return self.create_user(email=email, role=settings.ADMIN,
                                **extra_fields)

    def all(self):
        return self.get_queryset()


class User(AbstractBaseUser):
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=40, unique=True)
    bio = models.TextField(blank=True, null=True,)
    role = models.CharField(max_length=10, choices=settings.ROLES, blank=True,
                            default=settings.USER)
    password = models.CharField(max_length=128, verbose_name='password',
                                blank=True)
    confirmation_code = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == settings.ADMIN

    @property
    def is_not_user(self):
        return self.role != settings.USER


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
        blank=True,
        null=True,
        db_index=True,
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='titles'
    )

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

    class Meta:
        ordering = ('name',)

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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


SCORE_CHOICES = zip(range(1, 11), range(1, 11))


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
