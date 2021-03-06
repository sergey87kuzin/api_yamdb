from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validator_year


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email=email, role=settings.ADMIN, password=password,
            **extra_fields
        )

    def all(self):
        return self.get_queryset()


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, blank=True, null=True,
                                  verbose_name='first_name')
    last_name = models.CharField(max_length=30, blank=True,
                                 verbose_name='last_name')
    username = models.CharField(max_length=40, unique=True,
                                verbose_name='username')
    bio = models.TextField(blank=True, null=True, verbose_name='biography')
    role = models.CharField(max_length=10, choices=settings.ROLES, blank=True,
                            default=settings.ADMIN, verbose_name='role')
    password = models.CharField(max_length=128, verbose_name='password',
                                blank=True)
    confirmation_code = models.CharField(max_length=30, blank=True,
                                         verbose_name='token')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-id',)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == settings.ADMIN

    @property
    def is_admin(self):
        return self.role == settings.ADMIN

    @property
    def is_not_user(self):
        return self.role != settings.USER


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


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='???????????????? ????????????????????????',
    )
    year = models.IntegerField(
        verbose_name='?????? ??????????????',
        blank=True,
        null=True,
        db_index=True,
        validators=[validator_year]
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='????????????????',
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        verbose_name='????????',
        related_name='titles',
    )

    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='??????????????????',
        related_name='titles',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    class Meta:
        verbose_name = '????????????????????????'
        verbose_name_plural = '????????????????????????'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='???????????????? ??????????????????',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = '??????????????????'
        verbose_name_plural = '??????????????????'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='???????????????? ??????????',
        max_length=200,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = '????????'
        verbose_name_plural = '??????????'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='??????????')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='???????????? ????????????????????????',
        validators=[
            MinValueValidator(1, '???????????? ???? ?????????? ???????? ???????????? 1'),
            MaxValueValidator(10, '???????????? ???? ?????????? ???????? ???????? 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='???????? ????????????????????', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        verbose_name = "??????????"
        verbose_name_plural = "????????????"
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name='??????????')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='???????? ????????????????????', auto_now_add=True
    )

    class Meta:
        verbose_name = "??????????????????????"
        verbose_name_plural = "??????????????????????"
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
