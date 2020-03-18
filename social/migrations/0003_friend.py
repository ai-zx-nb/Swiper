# Generated by Django 2.2.11 on 2020-03-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20200316_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='好友ID')),
                ('uid2', models.IntegerField(verbose_name='好友ID')),
            ],
            options={
                'unique_together': {('uid1', 'uid2')},
            },
        ),
    ]
