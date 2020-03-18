from django.db import models
from django.db import IntegrityError

from common import err


class Swiped(models.Model):
    '''滑动记录'''
    STYPES = (
        ('like', '右滑'),
        ('superlike', '上滑'),
        ('dislike', '左滑'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 ID')
    sid = models.IntegerField(verbose_name='被滑动者的 ID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ['uid', 'sid']

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''增加一次滑动记录'''
        if stype not in ['like', 'superlike', 'dislike']:
            raise err.StypeErr

        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise err.SwipeRepeatErr

    @classmethod
    def is_liked(cls, uid, sid):
        '''
        检查是否喜欢过某人

        返回值:
            喜欢 / 超级喜欢 -> True
            不喜欢 -> False
            未滑过 -> None
        '''
        like_stypes = ['like', 'superlike']

        try:
            swipe = cls.objects.get(uid=uid, sid=sid)
            return swipe.stype in like_stypes  # 曾经右滑或上滑过对方返回 True，否则返回 False
        except cls.DoesNotExist:
            return None  # 没有滑到过对方，返回 None


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @staticmethod
    def sort_uid(uid1, uid2):
        '''为 uid 排序'''
        if uid1 > uid2:
            return uid2, uid1
        else:
            return uid1, uid2

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        try:
            return cls.objects.create(uid1=uid1, uid2=uid2)
        except IntegrityError:
            pass

    @classmethod
    def break_off(cls, uid1, uid2):
        '''绝交'''
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_id_list(cls, uid):
        '''好友 ID 列表'''
        query_condition = models.Q(uid1=uid) | models.Q(uid2=uid)
        frd_record = cls.objects.filter(query_condition)
        fid_list = []
        for frd in frd_record:
            if frd.uid1 == uid:
                fid_list.append(frd.uid2)
            else:
                fid_list.append(frd.uid1)
        return fid_list
