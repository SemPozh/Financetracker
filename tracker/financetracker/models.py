from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Finance(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    money = models.FloatField(verbose_name='Деньги')
    date = models.DateField(verbose_name='Дата')
    is_income = models.BooleanField(verbose_name='Это доход')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Финанс'
        verbose_name_plural = 'Финансы'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Содержание')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    grade = models.FloatField(verbose_name='Оценка')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'





