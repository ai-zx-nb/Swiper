import datetime

from django.db import models
from django.db.models import query

from libs.cache import rds
from common.keys import MODEL_K


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Save the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # 调用原 save() 方法将数据保存到数据库
    self._save(force_insert, force_update, using, update_fields)

    # 将 model_obj 保存到 缓存中
    model_key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(model_key, self, 86400 * 7)


def get(self, *args, **kwargs):
    """
    Perform the query and return a single object matching the given
    keyword arguments.
    """
    # 取出 Model 类的名称
    cls_name = self.model.__name__

    # 检查 kwargs 中是否有 id 或 pk
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk is not None:
        model_key = MODEL_K % (cls_name, pk)  # 定义缓存 Key
        model_obj = rds.get(model_key)        # 从 Redis 中取出模型对象
        if isinstance(model_obj, self.model):
            return model_obj

    # 如果缓存中未取到 model 数据，则直接从数据库获取
    model_obj = self._get(*args, **kwargs)

    # 将取到的 model 对象保存到缓存
    model_key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(model_key, model_obj, 86400 * 7)

    return model_obj


def to_dict(self, exclude=()):
    '''将当前模型的属性转成 dict 类型'''
    attr_dict = {}

    # 需要强转成字符串的类型
    force_str_types = (datetime.datetime, datetime.date, datetime.time)

    for field in self._meta.fields:
        name = field.attname
        value = getattr(self, field.attname)

        if name not in exclude:
            # 将特殊类型强转成 str 类型
            if isinstance(value, force_str_types):
                value = str(value)
            attr_dict[name] = value

    return attr_dict


def patch_model():
    '''通过 Monkey Patch 的方式为 DjangoORM 增加缓存处理'''
    # 修改 Model 的 save 方法
    models.Model._save = models.Model.save
    models.Model.save = save

    # 修改 get 方法
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    # 统一为所有 Model 增加 to_dict 方法
    models.Model.to_dict = to_dict
