#!/usr/bin/env python
# coding=utf-8

import json
from bottle import delete, get, post, put
from common import convert_helper, web_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import positions_logic, department_logic, manager_logic, _common_logic


@get('/api/system/positions/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 部门id
    department_id = convert_helper.to_int0(web_helper.get_query('department_id', '部门id'))
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

    _positions_logic = positions_logic.PositionsLogic()
    # 读取记录
    wheres = ''
    if department_id:
        wheres = 'department_id=' + str(department_id)
    result = _positions_logic.get_list('*', wheres, page_number, page_size, order_by)
    if result:
        # 直接输出json
        return json.dumps(result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/positions/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _positions_logic = positions_logic.PositionsLogic()
    # 读取记录
    result = _positions_logic.get_model_for_cache(id)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/system/positions/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '角色名称')
    department_id = convert_helper.to_int0(web_helper.get_form('department_id', '部门id'))
    page_power = web_helper.get_form('page_power', '权限列表', is_check_null=False)

    _department_logic = department_logic.DepartmentLogic()
    # 读取对应的部门记录
    department_result = _department_logic.get_model_for_cache(department_id)
    if not department_result:
        return web_helper.return_msg(-1, "部门不存在")

    _positions_logic = positions_logic.PositionsLogic()
    # 组合更新字段
    fields = {
        'name': string(name),
        'department_id': department_id,
        'department_code': string(department_result.get('code', '')),
        'department_name': string(department_result.get('name', '')),
        'page_power': string(page_power),
    }
    # 读取记录
    result = _positions_logic.add_model(fields)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '提交成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/system/positions/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '角色名称')
    department_id = convert_helper.to_int0(web_helper.get_form('department_id', '部门id'))
    page_power = web_helper.get_form('page_power', '权限列表', is_check_null=False)
    if page_power == ',':
        page_power = ''

    _positions_logic = positions_logic.PositionsLogic()
    positions_result = _positions_logic.get_model_for_cache(id)
    if department_id != positions_result.get('department_id'):
        return web_helper.return_msg(-1, '该角色所属部门错误，请与管理员联系')

    # 组合更新字段
    fields = {
        'name': string(name),
        'page_power': string(page_power),
    }

    # 读取记录
    result = _positions_logic.edit_model(id, fields)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '提交成功', result)
    else:
        return web_helper.return_msg(-1, "提交失败")


@delete('/api/system/positions/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 判断要删除的记录是否被引用，是的话不能删除
    _manager_logic = manager_logic.ManagerLogic()
    if _manager_logic.exists('positions_id=' + str(id)):
        return web_helper.return_msg(-1, "当前职位已绑定相关管理员，不能直接删除")

    # 删除记录
    _positions_logic = positions_logic.PositionsLogic()
    result = _positions_logic.delete_model(id)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '删除成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
