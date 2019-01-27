#!/usr/bin/env python
# coding=utf-8

from logic import _logic_base
from common.string_helper import string
from config import db_config


class ManagerOperationLogLogic(_logic_base.LogicBase):
    """管理员操作日志管理表逻辑类"""

    def __init__(self):
        # 表名称
        self.__table_name = 'manager_operation_log'
        # 初始化
        _logic_base.LogicBase.__init__(self, db_config.DB, db_config.IS_OUTPUT_SQL, self.__table_name)


    def add_operation_log(self, manager_id, manager_name, ip, remark):
        """记录用户登录日志"""
        # 组合要更新的字段内容
        fields = {'manager_id':manager_id, 'manager_name':string(manager_name), 'ip':string(ip), 'remark':string(remark)}
        # 更新记录
        self.add_model(fields)
