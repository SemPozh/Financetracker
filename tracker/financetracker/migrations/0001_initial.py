# Generated by Django 3.2.5 on 2021-07-17 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('money', models.FloatField(verbose_name='Деньги')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('is_income', models.BooleanField(verbose_name='Это доход')),
                ('description', models.TextField(verbose_name='Описание')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Финанс',
                'verbose_name_plural': 'Финансы',
            },
        ),
    ]
