#!/usr/bin/env python
# coding=utf-8

import json
from bottle import get, put, post, delete
from common import web_helper, db_helper, convert_helper, json_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import product_class_logic, product_logic, _common_logic


@get('/api/product_class/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    # 排序字段
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    # 顺序还是倒序排序
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 类型
    type = web_helper.get_query('type', '类型', is_check_null=False)
    # 设置查询条件
    wheres = []
    # 判断是否是前台提交获取数据
    if type != 'backstage':
        wheres.append('is_enable=1')

    # 初始化排序字段
    orderby = None
    ### 设置排序 ###
    if sidx:
        orderby = sidx + ' ' + sord

    # 实例化product_class表操作类product_class_logic
    _product_class_logic = product_class_logic.ProductClassLogic()
    result = _product_class_logic.get_list('*', wheres, page_number, page_size, orderby)
    if result:
        return web_helper.return_raise(json.dumps(result, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/product_class/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 实例化product_class表操作类product_class_logic
    _product_class_logic = product_class_logic.ProductClassLogic()
    # 读取记录
    result = _product_class_logic.get_model_for_pk(id)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/product_class/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '分类名称')
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 设置新增参数
    fields = {
        'name': string(name),
        'is_enable': is_enable,
    }
    # 实例化product_class表操作类product_class_logic
    _product_class_logic = product_class_logic.ProductClassLogic()
    # 新增记录
    result = _product_class_logic.add_model(fields)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/product_class/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '分类名称')
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 设置新增参数
    fields = {
        'name': string(name),
        'is_enable': is_enable,
    }
    # 实例化product_class表操作类product_class_logic
    _product_class_logic = product_class_logic.ProductClassLogic()
    # 新增记录
    result = _product_class_logic.edit_model(id, fields)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@delete('/api/product_class/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    # 判断该分类是否已经被引用，是的话不能直接删除
    if _product_logic.exists('product_class_id=' + str(id)):
        return web_helper.return_msg(-1, "该分类已被引用，请清除对该分类的绑定后再来删除")

    # 实例化product_class表操作类product_class_logic
    _product_class_logic = product_class_logic.ProductClassLogic()
    result = _product_class_logic.delete_model(id)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
