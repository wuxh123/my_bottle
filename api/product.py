#!/usr/bin/env python
# coding=utf-8

import json
from bottle import get, put, post, delete
from common import web_helper, db_helper, convert_helper, json_helper, string_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import product_logic, _common_logic

@get('/api/product/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 产品分类id
    product_class_id = convert_helper.to_int0(web_helper.get_query('product_class_id', '产品分类id', is_check_null=False))
    # 类型
    type = web_helper.get_query('type', '类型', is_check_null=False)
    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    # 排序字段
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    # 顺序还是倒序排序
    sord = web_helper.get_query('sord', '', is_check_null=False)

    # 设置查询条件
    wheres = []
    if product_class_id > 0:
        wheres.append('product_class_id=' + str(product_class_id))
    # 判断是否是前台提交获取数据
    if type != 'backstage':
        wheres.append('is_enable=1')

    # 初始化排序字段
    orderby = None
    ### 设置排序 ###
    if sidx:
        orderby = sidx + ' ' + sord

    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    result = _product_logic.get_list('*,(select name from product_class where id=product_class_id) as product_class_name', wheres, page_number, page_size, orderby)
    if result:
        return web_helper.return_raise(json.dumps(result, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/product/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    # 执行get_model_for_pk()方法，获取记录实体
    model = _product_logic.get_model_for_pk(id)
    if model:
        return web_helper.return_msg(0, '查询成功', model)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/product/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '产品名称')
    code = web_helper.get_form('code', '产品编码')
    product_class_id = convert_helper.to_int0(web_helper.get_form('product_class_id', '产品分类'))
    standard = web_helper.get_form('standard', '产品规格')
    quality_guarantee_period = web_helper.get_form('quality_guarantee_period', '保质期')
    place_of_origin = web_helper.get_form('place_of_origin', '产地')
    front_cover_img = web_helper.get_form('front_cover_img', '封面图片')
    content = web_helper.get_form('content', '产品描述', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 设置新增参数
    fields = {
        'name': string(name),
        'code': string(code),
        'product_class_id': product_class_id,
        'standard': string(standard),
        'quality_guarantee_period': string(quality_guarantee_period),
        'place_of_origin': string(place_of_origin),
        'front_cover_img': string(front_cover_img),
        'content': string(content),
        'is_enable': is_enable,
    }
    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    # 新增记录
    result = _product_logic.add_model(fields)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/product/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '产品名称')
    code = web_helper.get_form('code', '产品编码')
    product_class_id = convert_helper.to_int0(web_helper.get_form('product_class_id', '产品分类'))
    standard = web_helper.get_form('standard', '产品规格')
    quality_guarantee_period = web_helper.get_form('quality_guarantee_period', '保质期')
    place_of_origin = web_helper.get_form('place_of_origin', '产地')
    front_cover_img = web_helper.get_form('front_cover_img', '封面图片')
    content = web_helper.get_form('content', '产品描述', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)
    is_enable = convert_helper.to_int0(web_helper.get_form('is_enable', '是否启用'))

    # 设置新增参数
    fields = {
        'name': string(name),
        'code': string(code),
        'product_class_id': product_class_id,
        'standard': string(standard),
        'quality_guarantee_period': string(quality_guarantee_period),
        'place_of_origin': string(place_of_origin),
        'front_cover_img': string(front_cover_img),
        'content': string(content),
        'is_enable': is_enable,
    }
    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    # 修改记录
    result = _product_logic.edit_model(id, fields)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@delete('/api/product/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 实例化product表操作类ProductLogic
    _product_logic = product_logic.ProductLogic()
    result = _product_logic.delete_model(id)
    # 判断是否提交成功
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
