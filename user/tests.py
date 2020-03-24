import datetime

from django.test import TestCase

from user.models import User
from vip.models import Vip, Permission, VipPermRelation


def init_permission():
    '''创建权限模型'''
    permissions = (
        ('vipflag',       '会员身份标识'),
        ('superlike',     '超级喜欢'),
        ('rewind',        '反悔功能'),
        ('anylocation',   '任意更改定位'),
        ('unlimit_like',  '无限喜欢次数'),
        ('who_liked_me',  '查看喜欢过我的人'),
    )

    for name, description in permissions:
        perm, _ = Permission.objects.get_or_create(name=name, description=description)
        print('create permission %s' % perm.name)


def init_vip():
    vip_data = (
        ('非会员', 0, 36500, 0),

        ('青铜会员(月卡)', 1, 30, 10),
        ('青铜会员(季卡)', 1, 180, 50),
        ('青铜会员(年卡)', 1, 365, 90),

        ('白银会员(月卡)', 2, 30, 20),
        ('白银会员(季卡)', 2, 180, 100),
        ('白银会员(年卡)', 2, 365, 180),

        ('黄金会员(月卡)', 3, 30, 40),
        ('黄金会员(季卡)', 3, 180, 200),
        ('黄金会员(年卡)', 3, 365, 360),
    )
    for name, level, dur, price in vip_data:
        vip, _ = Vip.objects.get_or_create(
            name=name,
            level=level,
            duration=dur,
            price=price
        )
        print('create %s' % vip.name)


def create_vip_perm_relations():
    '''创建 Vip 和 Permission 的关系'''
    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')
    who_liked_me = Permission.objects.get(name='who_liked_me')

    # 给 VIP 1 分配权限
    VipPermRelation.objects.get_or_create(vip_level=1, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_level=1, perm_id=superlike.id)

    # 给 VIP 2 分配权限
    VipPermRelation.objects.get_or_create(vip_level=2, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_level=2, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_level=2, perm_id=rewind.id)

    # 给 VIP 3 分配权限
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=anylocation.id)
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=unlimit_like.id)
    VipPermRelation.objects.get_or_create(vip_level=3, perm_id=who_liked_me.id)


def create_vip():
    init_permission()
    init_vip()
    create_vip_perm_relations()


class UserTest(TestCase):
    def setUp(self):
        create_vip()
        user = User.objects.create(phonenum='test', nickname='TestUser')

    def test_vip(self):
        user = User.objects.get(phonenum='test')

        # 检查 VIP 默认等级
        self.assertEqual(user.vip.level, 0)

        # 检查 VIP 设置方法
        user.set_vip(9)

        self.assertEqual(user.vip_id, 9)
        self.assertEqual(user.vip.level, 3)

        now = datetime.datetime.now() + datetime.timedelta(180)
        self.assertAlmostEqual(user.vip_end, now, delta=datetime.timedelta(seconds=1))
