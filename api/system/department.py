#!/usr/bin/env python
# coding=utf-8

import json
from bottle import delete, get, post, put
from common import convert_helper, web_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import department_logic, positions_logic, _common_logic


@get('/api/system/department/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 父id
    parent_id = convert_helper.to_int0(web_helper.get_query('nodeid', '', is_check_null=False))
    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面页码与显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    # 接收排序参数
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 初始化排序字段
    order_by = 'sort asc'
    if sidx:
        order_by = sidx + ' ' + sord

    _department_logic = department_logic.DepartmentLogic()
    # 读取记录
    wheres = 'parent_id=' + str(parent_id)
    result = _department_logic.get_list('*', wheres, page_number, page_size, order_by)
    if result:
        return json.dumps(result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/department/tree/')
@exception_handling
def callback():
    """
    获取列表数据（树列表）
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _department_logic = department_logic.DepartmentLogic()
    # 读取记录
    result = _department_logic.get_list('id, parent_id, name, not is_leaf as open')
    if result:
        return web_helper.return_msg(0, "成功", {'tree_list': result.get('rows')})
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/department/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _department_logic = department_logic.DepartmentLogic()
    # 读取记录
    result = _department_logic.get_model_for_cache(id)
    if result:
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/system/department/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '部门名称')
    parent_id = convert_helper.to_int0(web_helper.get_form('parent_id', '父id', is_check_null=False))
    sort = convert_helper.to_int0(web_helper.get_form('sort', '排序', is_check_null=False))
    is_leaf = web_helper.get_form('is_leaf', '是否最终节点', is_check_null=False)

    _department_logic = department_logic.DepartmentLogic()
    # 计算深度级别，即当前部门在哪一级；并生成部门编码
    if parent_id == 0:
        level = 0
        code = _department_logic.create_code('')
    else:
        model = _department_logic.get_model_for_cache(parent_id)
        if not model:
            return web_helper.return_msg(-1, "您选择的部门不存在")

        level = model.get('level', 0) + 1
        code = _department_logic.create_code(model.get('code', ''))
    # 如果没有设置排序，则自动获取当前级别最大的序号加1
    if sort == 0:
        sort = _department_logic.get_max('parent_id', 'parent_id=' + str(parent_id)) + 1

    # 组合更新字段
    fields = {
        'name': string(name),
        'code': string(code),
        'parent_id': parent_id,
        'sort': sort,
        'level': level,
        'is_leaf': is_leaf,
    }
    # 新增记录
    result = _department_logic.add_model(fields)
    if result:
        return web_helper.return_msg(0, '提交成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/system/department/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '部门名称')
    parent_id = convert_helper.to_int0(web_helper.get_form('parent_id', '父id', is_check_null=False))
    sort = convert_helper.to_int0(web_helper.get_form('sort', '排序', is_check_null=False))
    is_leaf = web_helper.get_form('is_leaf', '是否最终节点', is_check_null=False)

    _department_logic = department_logic.DepartmentLogic()
    # 如果没有设置排序，则自动获取当前级别最大的序号加1
    if sort == 0:
        sort = _department_logic.get_max('parent_id', 'parent_id=' + str(parent_id)) + 1

    # 组合更新字段
    fields = {
        'name': string(name),
        'sort': sort,
        'is_leaf': is_leaf,
    }
    # 修改记录
    result = _department_logic.edit_model(id, fields)
    if result:
        return web_helper.return_msg(0, '提交成功', result)
    else:
        return web_helper.return_msg(-1, "提交查询失败")


@delete('/api/system/department/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _department_logic = department_logic.DepartmentLogic()
    # 判断要删除的节点是否有子节点，是的话不能删除
    if _department_logic.exists('parent_id=' + str(id)):
        return web_helper.return_msg(-1, "当前部门下已存在子部门，不能直接删除")
    # 判断要删除的记录是否被引用，是的话不能删除
    _positions_logic = positions_logic.PositionsLogic()
    if _positions_logic.exists('department_id=' + str(id)):
        return web_helper.return_msg(-1, "当前部门已存在相关职位，不能直接删除")

    # 删除记录
    result = _department_logic.delete_model(id)
    if result:
        return web_helper.return_msg(0, '删除成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
