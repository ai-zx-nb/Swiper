# Generated by Django 2.2.11 on 2020-03-11 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phonenum',
            field=models.CharField(max_length=15, unique=True, verbose_name='手机号'),
        ),
    ]
