#!/usr/bin/env python
# coding=utf-8

from bottle import request, get
from common import web_helper
from common.except_helper import exception_handling
from logic import manager_operation_log_logic

@get('/api/logout/')
@exception_handling
def logout():
    """退出系统"""
    s = request.environ.get('beaker.session')
    try:
        # 添加退出登录日志
        _manager_operation_log_logic = manager_operation_log_logic.ManagerOperationLogLogic()
        _manager_operation_log_logic.add_operation_log(s.get('id', 0), s.get('name', ''), web_helper.get_ip(), '【' + s.get('name', '') + '】退出登录')

        s.delete()
    except Exception:
        pass
    return web_helper.return_msg(0, '成功')
