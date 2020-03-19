from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=20, unique=True, verbose_name='会员名称')
    level = models.IntegerField(default=0, verbose_name='会员等级')
    price = models.FloatField(verbose_name='会员价格')
    duration = models.IntegerField(verbose_name='会员时长')

    def has_perm(self, perm_name):
        '''检查当前 VIP 是否具有某权限'''
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_level=self.level, perm_id=perm.id).exists()


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=20, unique=True, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述')


class VipPermRelation(models.Model):
    '''会员、权限关系表'''
    vip_level = models.IntegerField(verbose_name='会员等级')
    perm_id = models.IntegerField(verbose_name='权限ID')
