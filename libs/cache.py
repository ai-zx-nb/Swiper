from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from redis import Redis as _Redis

from swiper.conf import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.
        """
        pickled_data = dumps(value)  # 将需要保存到 Redis 中的值进行序列化
        return super().set(name, pickled_data, ex, px, nx, xx)

    def get(self, name, default=None):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        pickled_data = super().get(name)
        if pickled_data is None:
            return default
        else:
            try:
                value = loads(pickled_data)
            except UnpicklingError:
                return pickled_data
            else:
                return value

    def hmset(self, name, mapping):
        '''
        Set key to value within hash ``name`` for each corresponding
        key and value from the ``mapping`` dict.
        '''
        for k, v in mapping.items():
            mapping[k] = dumps(v, HIGHEST_PROTOCOL)
        return super().hmset(name, mapping)


    def hmget(self, name, keys, *args):
        """Returns a list of values ordered identically to ``keys``"""
        values_list = super().hmget(name, keys, *args)
        for idx, value in enumerate(values_list):
            if value is not None:
                try:
                    values_list[idx] = loads(value)
                except UnpicklingError:
                    pass
        return values_list

    def hgetall(self, name):
        "Return a Python dict of the hash's name/value pairs"
        mapping = super().hgetall(name)
        for k, v in mapping.items():
            try:
                mapping[k] = loads(v)
            except UnpicklingError:
                pass
        return mapping


rds = Redis(**REDIS)  # Redis 连接的单例
