#!/usr/bin/env python
# coding=utf-8

import redis
import datetime

from common import log_helper
from config import redis_config

# 设置redis配置参数
_redis = redis_config.REDIS
# 初始化Redis缓存链接
r = None
try:
    if not r:
        r = redis.Redis(host=_redis.get('server', ''),
                        port=_redis.get('post', ''),
                        db=_redis.get('db', ''),
                        password=_redis.get('pwd', ''),
                        socket_timeout=1,
                        socket_connect_timeout=1)
except Exception as e:
    log_helper.info('连接redis出错:(' + str(_redis) + ')' + str(e.args))
    pass


def set(key, value, time=86400):
    """
    写缓存
    :param key: 缓存key，字符串，不区分大小写
    :param value: 要存储的值
    :param time: 缓存过期时间（单位：秒），0=永不过期
    :return:
    """
    # 将key转换为小写字母
    key = str(key).lower()
    try:
        r.set(key, value, time)
    except Exception as e:
        log_helper.info('写缓存失败:key(' + key + ')' + str(e.args))
        pass


def get(key):
    """
    读缓存
    :param key: 缓存key，字符串，不区分大小写
    :return:
    """
    # 将key转换为小写字母
    key = str(key).lower()
    try:
        value = r.get(key)
    except Exception as e:
        # log_helper.error('读缓存失败:key(' + key + ')' + str(e.args) + ' r:' + str(r) + ' _redis:' + str(_redis))
        value = None

    return _str_to_json(value)


def push(key, value):
    """
    添加数据到队列头部
    :param key: 缓存key，字符串，不区分大小写
    :param value: 要存储的值
    """
    # 将key转换为小写字母
    key = str(key).lower()
    try:
        r.lpush(key, value)
    except Exception as e:
        log_helper.info('写缓存失败:key(' + key + ')' + str(e.args))
        pass


def pop(key):
    """
    从缓存队列的后尾读取一条数据
    :param key: 缓存key，字符串，不区分大小写
    :return: 缓存数据
    """
    # 将key转换为小写字母
    key = str(key).lower()
    try:
        value = r.rpop(key)
    except Exception as e:
        log_helper.info('读取缓存队列失败:key(' + key + ')' + str(e.args))
        value = None

    return _str_to_json(value)


def _str_to_json(value):
    """
    将缓存中读取出来的字符串转换成对应的数据、元组、列表或字典
    """
    if not value:
        return value
    # 否则直接转换
    try:
        value = value.decode()
        return eval(value)
    except Exception as e:
        print(e.args)
        pass
    # 否则直接输出字符串
    return value


def delete(key):
    """
    删除缓存
    :param key:缓存key，字符串，不区分大小写
    :return:
    """
    # 将key转换为小写字母
    key = str(key).lower()
    try:
        log_helper.info(str(r.delete(key)))
    except Exception as e:
        log_helper.info('Exception:' + str(e.args))
        pass


def clear():
    """
    清空所有缓存
    """
    try:
        r.flushdb()
    except:
        pass
