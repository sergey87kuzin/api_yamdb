import django.core.validators
import django.db.models.deletion


import api.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('role', models.CharField(blank=True, choices=[('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user')], default='user', max_length=10)),
                ('password', models.CharField(blank=True, max_length=128, verbose_name='password')),
                ('confirmation_code', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(max_length=40, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last_name')),
                ('username', models.CharField(max_length=40, unique=True, verbose_name='username')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='biography')),
                ('role', models.CharField(blank=True, choices=[('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user')], default='user', max_length=10, verbose_name='role')),
                ('password', models.CharField(blank=True, max_length=128, verbose_name='password')),
                ('confirmation_code', models.CharField(blank=True, max_length=30, verbose_name='token')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название жанра')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название произведения')),
                ('year', models.IntegerField(blank=True, db_index=True, null=True, validators=[api.validators.validator_year], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='api.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='api.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка произведения')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.title')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.review')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
    ]

