#!/usr/bin/env python
# coding=utf-8

from logic import _logic_base
from config import db_config


class PositionsLogic(_logic_base.LogicBase):
    """职位管理表逻辑类"""

    def __init__(self):
        # 表名称
        self.__table_name = 'positions'
        # 初始化
        _logic_base.LogicBase.__init__(self, db_config.DB, db_config.IS_OUTPUT_SQL, self.__table_name)


    def get_page_power(self, positions_id):
        """获取当前用户权限"""
        page_power = self.get_value_for_cache(positions_id, 'page_power')
        if page_power:
            return ',' + page_power + ','
        else:
            return ','