#!/usr/bin/env python
# coding=utf-8

from common import cache_helper, convert_helper, encrypt_helper


def check_operation_times(operation_name, limiting_frequency, ip, is_add=True):
    """
    检查操作次数
    参数：
    operation_name      操作名称
    limiting_frequency  限制次数
    is_add              是否累加
    返回参数：
    True    不限制
    False   限制操作
    """
    if not operation_name or limiting_frequency is None:
        return False, '参数错误，错误码：-400-001，请与管理员联系', '', 0

    # 如果限制次数为0时，默认不限制操作
    if limiting_frequency <= 0:
        return True, '', '', 0

    ##############################################################
    ### 判断用户操作次数，超出次数限制执行 ###
    # 获取当前用户已记录操作次数
    operation_times_key = operation_name + '_' + encrypt_helper.md5(operation_name + ip)
    operation_times = convert_helper.to_int0(cache_helper.get(operation_times_key))

    # 如果系统限制了出错次数，且当前用户已超出限制，则返回错误
    if limiting_frequency and operation_times >= limiting_frequency:
        return False, '您在10分钟内连续操作次数达到' + str(limiting_frequency) + '次，已超出限制，请稍候再试', operation_times_key, operation_times

    if is_add:
        # 记录操作次数，默认在缓存中存储10分钟
        cache_helper.set(operation_times_key, operation_times + 1, 600)

    return True, '', operation_times_key, operation_times


def add_operation_times(operation_times_key):
    """
    累加操作次数
    参数：
    operation_times_key 缓存key
    """
    # 获取当前用户已记录操作次数
    get_operation_times = convert_helper.to_int0(cache_helper.get(operation_times_key))
    # 记录获取次数
    cache_helper.set(operation_times_key, get_operation_times + 1, 600)


def del_operation_times(operation_times_key):
    """
    清除操作次数
    参数：
    operation_times_key 缓存key
    """
    # 记录获取次数
    cache_helper.delete(operation_times_key)


def check_login_power(id, k, t, sessionid):
    """
    检查拨号小信接口，验证用户是否有权限访问
    :param id: 用户id
    :param k:  32位长度的密钥串
    :param t:  时间戳
    :param sessionid: 当前用户的密钥
    :return: False=验证失败，True=验证成功
    """
    if not sessionid:
        return False

    return encrypt_helper.md5(str(id) + sessionid + str(t) + sessionid + str(id)) == k
