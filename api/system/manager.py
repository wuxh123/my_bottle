#!/usr/bin/env python
# coding=utf-8

import json
from bottle import delete, get, post, put
from common import convert_helper, json_helper, web_helper, string_helper, encrypt_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import manager_logic, department_logic, positions_logic, _common_logic


@get('/api/system/manager/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面页码与显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 初始化排序字段
    order_by = 'id asc'
    if sidx:
        order_by = sidx + ' ' + sord

    _manager_logic = manager_logic.ManagerLogic()
    # 读取记录
    result = _manager_logic.get_list('*', '', page_number, page_size, order_by)
    if result:
        return json.dumps(result, cls=json_helper.CJsonEncoder)
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/manager/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _manager_logic = manager_logic.ManagerLogic()
    # 读取记录
    result = _manager_logic.get_model_for_cache(id)
    if result:
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/system/manager/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '管理员名称')
    sex = web_helper.get_form('sex', '性别', is_check_null=False)
    if sex != '男':
        sex = '女'
    mobile = web_helper.get_form('mobile', '手机号码', is_check_null=False)
    if mobile and not string_helper.is_mobile(mobile):
        return web_helper.return_msg(-1, '手机号码格式不正确')
    birthday = web_helper.get_form('birthday', '出生日期', is_check_null=False)
    if birthday:
        birthday = convert_helper.to_date(birthday)
    email = web_helper.get_form('email', 'email', is_check_null=False)
    if email and not string_helper.is_email(email):
        return web_helper.return_msg(-1, 'Email格式不正确')
    remark = web_helper.get_form('remark', '备注', is_check_null=False)
    department_id = convert_helper.to_int0(web_helper.get_form('department_id', '所属部门'))
    positions_id = convert_helper.to_int0(web_helper.get_form('positions_id', '所属职位'))
    is_work = convert_helper.to_int0(web_helper.get_form('is_work', '工作状态'))
    is_enabled = web_helper.get_form('is_enabled', '是否启用', is_check_null=False)
    login_name = web_helper.get_form('login_name', '登录账号')
    login_password = web_helper.get_form('login_password1', '登录密码', is_check_special_char=False)
    if len(login_password) < 6:
        return web_helper.return_msg(-1, '登录密码长度必须大于等于6位')
    login_password = encrypt_helper.md5(encrypt_helper.md5(login_password)[2:24])

    # 判断提交的部门id是否正确
    _department_logic = department_logic.DepartmentLogic()
    department_result = _department_logic.get_model_for_cache(department_id)
    if not department_result:
        return web_helper.return_msg(-1, '所属部门不存在')
    # 判断提交的职位id是否正确
    _positions_logic = positions_logic.PositionsLogic()
    positions_result = _positions_logic.get_model_for_cache(positions_id)
    if not positions_result or positions_result.get('department_id') != department_id:
        return web_helper.return_msg(-1, '所属职位不存在')

    _manager_logic = manager_logic.ManagerLogic()
    # 组合更新字段
    fields = {
        'name': string(name),
        'sex': string(sex),
        'mobile': string(mobile),
        'email': string(email),
        'remark': string(remark),
        'department_id': department_id,
        'department_code': string(department_result.get('code', '')),
        'department_name': string(department_result.get('name', '')),
        'positions_id': positions_id,
        'positions_name': string(positions_result.get('name', '')),
        'is_work': is_work,
        'is_enabled': is_enabled,
        'login_name': string(login_name),
        'login_password': string(login_password),
    }
    if birthday:
        fields['birthday'] = string(str(birthday))
    # 添加记录
    result = _manager_logic.add_model(fields)
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/system/manager/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '管理员名称')
    sex = web_helper.get_form('sex', '性别', is_check_null=False)
    if sex != '男':
        sex = '女'
    mobile = web_helper.get_form('mobile', '手机号码', is_check_null=False)
    if mobile and not string_helper.is_mobile(mobile):
        return web_helper.return_msg(-1, '手机号码格式不正确')
    birthday = web_helper.get_form('birthday', '出生日期', is_check_null=False)
    if birthday:
        birthday = convert_helper.to_date(birthday)
    email = web_helper.get_form('email', 'email', is_check_null=False)
    if email and not string_helper.is_email(email):
        return web_helper.return_msg(-1, 'Email格式不正确')
    remark = web_helper.get_form('remark', '备注', is_check_null=False)
    department_id = convert_helper.to_int0(web_helper.get_form('department_id', '所属部门'))
    positions_id = convert_helper.to_int0(web_helper.get_form('positions_id', '所属职位'))
    is_work = web_helper.get_form('is_work', '工作状态')
    is_enabled = web_helper.get_form('is_enabled', '是否启用', is_check_null=False)
    login_name = web_helper.get_form('login_name', '登录账号')
    login_password1 = web_helper.get_form('login_password1', '新密码', is_check_null=False, is_check_special_char=False)
    # 判断用户是否修改密码
    if login_password1:
        if len(login_password1) < 6:
            return web_helper.return_msg(-1, '新密码长度必须大于等于6位')
        login_password1 = encrypt_helper.md5(encrypt_helper.md5(login_password1)[2:24])

    # 判断提交的部门id是否正确
    _department_logic = department_logic.DepartmentLogic()
    department_result = _department_logic.get_model_for_cache(department_id)
    if not department_result:
        return web_helper.return_msg(-1, '所属部门不存在')
    # 判断提交的职位id是否正确
    _positions_logic = positions_logic.PositionsLogic()
    positions_result = _positions_logic.get_model_for_cache(positions_id)
    if not positions_result or positions_result.get('department_id') != department_id:
        return web_helper.return_msg(-1, '所属职位不存在')

    _manager_logic = manager_logic.ManagerLogic()
    result = _manager_logic.get_model_for_cache(id)
    if not result:
        return web_helper.return_msg(-1, '管理员账号不存在')

    # 组合更新字段
    fields = {
        'name': string(name),
        'sex': string(sex),
        'mobile': string(mobile),
        'email': string(email),
        'remark': string(remark),
        'department_id': department_id,
        'department_code': string(department_result.get('code', '')),
        'department_name': string(department_result.get('name', '')),
        'positions_id': positions_id,
        'positions_name': string(positions_result.get('name', '')),
        'is_work': is_work,
        'is_enabled': is_enabled,
        'login_name': string(login_name),
    }
    if birthday:
        fields['birthday'] = string(str(birthday))
    if login_password1:
        fields['login_password'] = string(login_password1)
    # 修改记录
    result = _manager_logic.edit_model(id, fields)
    if result:
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/system/manager/<id:int>/dimission/')
@exception_handling
def callback(id):
    """
    设置用户离职
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _manager_logic = manager_logic.ManagerLogic()
    fields = {
        'is_work': False,
        'is_enabled': False,
    }
    # 读取记录
    result = _manager_logic.edit_model(id, fields)
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "管理员不存在")


@put('/api/system/manager/<id:int>/reinstated/')
@exception_handling
def callback(id):
    """
    设置用户复职
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _manager_logic = manager_logic.ManagerLogic()
    # 读取记录
    result = _manager_logic.get_model_for_cache(id)
    if result:
        if result.get('is_work'):
            return web_helper.return_msg(-1, '该管理员工作状态正常，不需要复职')

        fields = {
            'is_work': True,
            'is_enabled': True,
        }
        # 读取记录
        result = _manager_logic.edit_model(id, fields)
        if result:
            return web_helper.return_msg(0, '成功')

    return web_helper.return_msg(-1, "管理员不存在")


@delete('/api/system/manager/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _manager_logic = manager_logic.ManagerLogic()
    # 删除记录
    result = _manager_logic.get_model_for_cache(id)
    if result:
        # 未离职管理员不能直接删除
        if result.get('is_work') == 1:
            return web_helper.return_msg(-1, '未离职管理员不能直接删除')

        result = _manager_logic.delete_model(id)
        if result:
            return web_helper.return_msg(0, '删除成功')

    return web_helper.return_msg(-1, "删除失败")
