# Generated by Django 2.2.11 on 2020-03-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200311_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], default='male', max_length=10, verbose_name='匹配的性别')),
                ('dating_location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('郑州', '郑州'), ('西安', '西安'), ('武汉', '武汉'), ('成都', '成都'), ('沈阳', '沈阳')], default='北京', max_length=10, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=1, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=10, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=20, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matched', models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('郑州', '郑州'), ('西安', '西安'), ('武汉', '武汉'), ('成都', '成都'), ('沈阳', '沈阳')], default='北京', max_length=10, verbose_name='常居地'),
        ),
    ]