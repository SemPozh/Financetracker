# Generated by Django 3.2.5 on 2021-07-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financetracker', '0003_auto_20210724_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finance',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
    ]
