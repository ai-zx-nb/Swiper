import datetime

from django.db import models

from vip.models import Vip


class User(models.Model):
    GENDER = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('郑州', '郑州'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('成都', '成都'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER, default='male', verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象的 URL')
    location = models.CharField(max_length=10, default='北京', choices=LOCATION, verbose_name='常居地')

    vip_id = models.IntegerField(default=1, verbose_name='用户对应的会员ID')
    vip_end = models.DateTimeField(default='2222-02-22', verbose_name='会员过期时间')

    @property
    def profile(self):
        '''用户对应的 Profile'''
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''用户对应的 Vip'''
        if self.is_vip_expired():
            # 如果用户 VIP 已过期，直接将用户的 Vip ID 设置为非会员
            self.set_vip(1)

        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def set_vip(self, vip_id):
        '''为用户设置 Vip'''
        # 取出 Vip 数据
        vip = Vip.objects.get(id=vip_id)

        # 修改用户数据，并保存
        self.vip_id = vip_id
        self.vip_end = datetime.datetime.now() + datetime.timedelta(vip.duration)
        self._vip = vip
        self.save()

    def is_vip_expired(self):
        '''检查 Vip 是否过期'''
        now = datetime.datetime.now()
        return now >= self.vip_end

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    '''交友资料'''
    dating_gender = models.CharField(max_length=10, choices=User.GENDER, default='female',
                                     verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=10, default='北京', choices=User.LOCATION,
                                       verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=20, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    def to_dict(self):
        return {
            'id': self.id,
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
