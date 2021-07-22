from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Finance(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    money = models.FloatField(verbose_name='Деньги')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    is_income = models.BooleanField(verbose_name='Это доход')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Финанс'
        verbose_name_plural = 'Финансы'





