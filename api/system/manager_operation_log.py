#!/usr/bin/env python
# coding=utf-8

import json
from bottle import get
from common import convert_helper, datetime_helper, web_helper, json_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import manager_operation_log_logic, _common_logic


@get('/api/system/manager_operation_log/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 查询条件
    wheres = []
    start_time = convert_helper.to_date(web_helper.get_query('start_time', '开始时间', is_check_null=False))
    if start_time:
        wheres.append('add_time>=' + string(start_time))
    end_time = convert_helper.to_date(web_helper.get_query('end_time', '结束时间', is_check_null=False))
    if end_time:
        end_time = datetime_helper.timedelta('d', end_time, 1)
        wheres.append('add_time<' + string(end_time))
    manager_name = web_helper.get_query('manager_name', '管理员姓名', is_check_null=False)
    if manager_name:
        wheres.append('manager_name like \'%' + manager_name + '%\'')
    ip = web_helper.get_query('ip', 'ip', is_check_null=False)
    if ip:
        wheres.append('ip like \'' + ip + '%\'')
    remark = web_helper.get_query('remark', '操作内容', is_check_null=False)
    if remark:
        wheres.append('remark like \'%' + remark + '%\'')

    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面页码与显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 初始化排序字段
    order_by = 'id desc'
    if sidx:
        order_by = sidx + ' ' + sord

    _manager_operation_log_logic = manager_operation_log_logic.ManagerOperationLogLogic()
    # 读取记录
    result = _manager_operation_log_logic.get_list('*', wheres, page_number, page_size, order_by)
    if result:
        # 直接输出json
        return json.dumps(result, cls=json_helper.CJsonEncoder)
    else:
        return web_helper.return_msg(-1, "查询失败")

