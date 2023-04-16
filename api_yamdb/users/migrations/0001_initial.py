# Generated by Django 3.2 on 2023-02-28 15:32

import django.contrib.auth.models
import django.utils.timezone
import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='Как к Вам обращаться?', max_length=40, unique=True, validators=[users.validators.validate_username_not_me], verbose_name='Имя пользователя')),
                ('email', models.EmailField(help_text='Введите адрес электронной почты', max_length=254, verbose_name='адрес электронной почты')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], help_text='Выберите из списка роль для пользователя', max_length=50, verbose_name='Роль пользователя')),
                ('bio', models.TextField(blank=True, help_text='Выберите из списка роль для пользователя', max_length=250, verbose_name='Роль пользователя')),
                ('first_name', models.CharField(blank=True, help_text='Введите имя пользователя', max_length=100, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(blank=True, help_text='Введите Вашу фамилию', max_length=100, verbose_name='Фамилия пользователя')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='reviewuser',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_name'),
        ),
    ]