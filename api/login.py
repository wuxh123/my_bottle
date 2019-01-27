#!/usr/bin/env python
# coding=utf-8

from bottle import put
from bottle import post
from common import web_helper, encrypt_helper, security_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import manager_logic, manager_operation_log_logic


@put('/api/login/')
@exception_handling
def post_login():
    """用户登陆验证"""
    ##############################################################
    # 获取并验证客户端提交的参数
    ##############################################################
    print("^"*100)
    username = web_helper.get_form('username', '帐号')
    password = web_helper.get_form('password', '密码')
    verify = web_helper.get_form('verify', '验证码')
    ip = web_helper.get_ip()

    ##############################################################
    # 从session中读取验证码信息
    ##############################################################
    s = web_helper.get_session()
    verify_code = s.get('verify_code')
    # 删除session中的验证码（验证码每提交一次就失效）
    if 'verify_code' in s:
        del s['verify_code']
        s.save()
    # 判断用户提交的验证码和存储在session中的验证码是否相同
    if verify.upper() != verify_code:
        return web_helper.return_msg(-1, '验证码错误')

    ##############################################################
    ### 判断用户登录失败次数，超出次做登录限制 ###
    # 获取管理员登录密码错误限制次数，0=无限制，x次/小时
    limit_login_count = 10
    # 获取操作出错限制值
    is_ok, msg, operation_times_key, error_count = security_helper.check_operation_times('login_error_count', limit_login_count, web_helper.get_ip(), False)
    # 判断操作的出错次数是否已超出了限制
    if not is_ok:
        return web_helper.return_msg(-1, msg)

    ##############################################################
    ### 获取登录用户记录，并进行登录验证 ###
    ##############################################################
    # 初始化操作日志记录类
    _manager_operation_log_logic = manager_operation_log_logic.ManagerOperationLogLogic()
    # 初始化管理员逻辑类
    _manager_logic = manager_logic.ManagerLogic()
    # 从数据库中读取用户信息
    manager_result = _manager_logic.get_model_for_cache_of_where('login_name=' + string(username))
    # 判断用户记录是否存在
    if not manager_result:
        return web_helper.return_msg(-1, '账户不存在')

    # 获取管理员id
    manager_id =  manager_result.get('id', 0)
    # 获取管理员姓名
    manager_name = manager_result.get('name', '')

    ##############################################################
    ### 验证用户登录密码与状态 ###
    ##############################################################
    # 对客户端提交上来的验证进行md5加密将转为大写（为了密码的保密性，这里进行双重md5加密，加密时从第一次加密后的密串中提取一段字符串出来进行再次加密，提取的串大家可以自由设定）
    # pwd = encrypt_helper.md5(encrypt_helper.md5(password)[1:30]).upper()
    # 对客户端提交上来的验证进行md5加密将转为大写（只加密一次）
    pwd = encrypt_helper.md5(password).upper()
    # 检查登录密码输入是否正确
    if pwd != manager_result.get('login_password').upper():
        # 记录出错次数
        security_helper.add_operation_times(operation_times_key)
        # 记录日志
        _manager_operation_log_logic.add_operation_log(manager_id, manager_name, ip, '【' + manager_name + '】输入的登录密码错误')
        return web_helper.return_msg(-1, '密码错误')
    # 检查该账号虽否禁用了
    if not manager_result.get('is_enabled'):
        # 记录出错次数
        security_helper.add_operation_times(operation_times_key)
        # 记录日志
        _manager_operation_log_logic.add_operation_log(manager_id, manager_name, ip, '【' + manager_name + '】账号已被禁用，不能登录系统')
        return web_helper.return_msg(-1, '账号已被禁用')

    # 登录成功，清除登录错误记录
    security_helper.del_operation_times(operation_times_key)

    ##############################################################
    ### 把用户信息保存到session中 ###
    ##############################################################
    manager_id = manager_result.get('id')
    s['id'] = manager_id
    s['login_name'] = username
    s['name'] = manager_result.get('name')
    s['positions_id'] = manager_result.get('positions_id')
    s.save()

    ##############################################################
    ### 更新用户信息到数据库 ###
    ##############################################################
    # 更新当前管理员最后登录时间、Ip与登录次数（字段说明，请看数据字典）
    fields = {
        'last_login_time': 'now()',
        'last_login_ip': string(ip),
        'login_count': 'login_count+1',
    }
    # 写入数据库
    _manager_logic.edit_model(manager_id, fields)
    # 记录日志
    _manager_operation_log_logic.add_operation_log(manager_id, manager_name, ip, '【' + manager_name + '】登陆成功')

    return web_helper.return_msg(0, '登录成功')
