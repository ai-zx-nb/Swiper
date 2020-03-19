# Generated by Django 2.2.11 on 2020-03-19 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='权限名称')),
                ('description', models.TextField(verbose_name='权限描述')),
            ],
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='会员名称')),
                ('level', models.IntegerField(default=0, verbose_name='会员等级')),
                ('price', models.FloatField(verbose_name='会员价格')),
                ('duration', models.IntegerField(verbose_name='会员时长')),
            ],
        ),
        migrations.CreateModel(
            name='VipPermRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_level', models.IntegerField(verbose_name='会员等级')),
                ('perm_id', models.IntegerField(verbose_name='权限ID')),
            ],
        ),
    ]
