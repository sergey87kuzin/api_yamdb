from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

CHOICES = (('user', 'u'), ('moderator', 'm'), ('admin', 'a'),)


class UserManager(BaseUserManager):

    def create_user(self, email, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email, **extra_fields):
        return self.create_user(email=email, role='admin', **extra_fields)

    def all(self):
        return self.get_queryset()


class User(AbstractBaseUser):
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=40, unique=True)
    bio = models.TextField(blank=True, null=True,)
    role = models.CharField(max_length=10, choices=CHOICES, blank=True,
                            default='user')
    password = models.CharField(max_length=128, verbose_name='password',
                                blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

