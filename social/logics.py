import time
import datetime

from django.db.transaction import atomic

from swiper import conf
from common import err
from common import keys
from libs.cache import rds
from user.models import User
from social.models import Swiped
from social.models import Friend


def rcmd_users_from_q(uid):
    '''从优先推荐队列获取用户'''
    name = keys.FIRST_RCMD_Q % uid
    uid_list = rds.lrange(name, 0, 24)
    uid_list = [int(uid) for uid in uid_list]
    return User.objects.filter(id__in=uid_list)


def rcmd_users_from_db(uid, num):
    '''从数据库中获取推荐用户'''
    user = User.objects.get(id=uid)
    today = datetime.date.today()

    # 计算目标人群的出生日期范围
    earliest_birthday = today - datetime.timedelta(user.profile.max_dating_age * 365)
    latest_birthday = today - datetime.timedelta(user.profile.min_dating_age * 365)

    # 取出所有已滑过的用户的 ID 列表
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 从数据库中获取目标用户
    users = User.objects.filter(
        gender=user.profile.dating_gender,
        location=user.profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]  # 懒加载, Django 会解析完整语句, 然后拼接成一条 SQL, 然后发给 MySQL 执行

    return users


def rcmd_users(uid):
    '''为用户推荐一些可以交友的对象'''
    users_from_q = set(rcmd_users_from_q(uid))
    remain = 25 - len(users_from_q)
    users_from_db = set(rcmd_users_from_db(uid, remain))

    return users_from_q | users_from_db


def record_swipe_to_rds(uid, sid, stype):
    '''在执行滑动时，将必要数据写入 redis'''
    name = keys.FIRST_RCMD_Q % uid
    with rds.pipeline() as pipe:
        # 开启 Redis 事务
        pipe.watch(name, keys.HOT_RANK_K)
        pipe.multi()

        # 强制从 优先推荐队列 删除 sid
        pipe.lrem(name, 1, sid)

        # 处理滑动积分
        score = conf.SWIPE_SCORE[stype]
        pipe.zincrby(keys.HOT_RANK_K, score, sid)

        pipe.execute()


def like_someone(uid, sid):
    '''喜欢(右滑)了某人'''
    # 检查 sid 是否正确
    if not sid or uid == sid:
        raise err.SidErr('您的 SID 错了')

    Swiped.swipe(uid, sid, 'like')

    record_swipe_to_rds(uid, sid, 'like')

    # 检查对方是否 喜欢 过自己，如果是，匹配成好友
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢(上滑)了某人'''
    # 检查 sid 是否正确
    if not sid or uid == sid:
        raise err.SidErr('您的 SID 错了')

    Swiped.swipe(uid, sid, 'superlike')

    record_swipe_to_rds(uid, sid, 'superlike')

    # 检查对方是否 喜欢 过自己，如果是，匹配成好友
    is_liked = Swiped.is_liked(sid, uid)
    if is_liked == True:
        Friend.make_friends(uid, sid)
        return True
    elif is_liked is None:
        other_first_q = keys.FIRST_RCMD_Q % sid
        rds.rpush(other_first_q, uid)  # 将 UID 添加到对方的优先推荐队列
        return False
    else:
        return False


def dislike_someone(uid, sid):
    '''不喜欢(左滑)了某人'''
    # 检查 sid 是否正确
    if not sid or uid == sid:
        raise err.SidErr('您的 SID 错了')

    Swiped.swipe(uid, sid, 'dislike')

    record_swipe_to_rds(uid, sid, 'dislike')


def rewind_swipe(uid):
    '''
    反悔上一次的滑动

        Redis 中记录的数据: {
            'rewind_date': '2020-03-18',  # 反悔的日期
            'rewind_cnt': 0,              # 当天的反悔次数
        }
    '''
    # 从 Redis 中取出反悔数据
    rewind_key = 'Rewind-%s' % uid
    rewind_data = rds.hgetall(rewind_key)
    rewind_date = rewind_data.get(b'rewind_date', '1970-01-01')
    rewind_cnt = rewind_data.get(b'rewind_cnt', 0)

    # 取出当前时间
    now = datetime.datetime.today()
    today = str(now.date())

    # 检查当天 “反悔次数” 是否超过 3 次
    if today == rewind_date:
        if rewind_cnt >= 3:
            raise err.RewindLimitErr
    else:
        rewind_cnt = 0

    # 从数据库获取最后一条滑动记录, 并检查是否为 None
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')
    if last_swipe is None:
        raise err.NonSwipe

    # 检查时间是否超过 5 分钟
    if (now - last_swipe.stime) > datetime.timedelta(minutes=5):
        raise err.RewindTimeout

    # 操作时开启事务
    with atomic():
        # 之前匹配成好友，需要解除好友关系
        if last_swipe.stype in ['like', 'superlike']:
            Friend.break_off(uid, last_swipe.sid)

        # 删除滑动记录
        last_swipe.delete()

        # 之前是超级喜欢，需要将 ID 从对方推荐队列删除
        rds.lrem(keys.FIRST_RCMD_Q % last_swipe.sid, 0, uid)

        # 更新反悔数据
        rds.hmset(rewind_key, {'rewind_cnt': rewind_cnt + 1, 'rewind_date': today})


def who_liked_me(uid):
    '''过滤出喜欢过我，但是我还没有滑过的人'''
    # 取出我已经滑过的 sid 列表
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 取出 uid 列表
    uid_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike'])\
                             .exclude(uid__in=sid_list)\
                             .values_list('uid', flat=True)

    return User.objects.filter(id__in=uid_list)
