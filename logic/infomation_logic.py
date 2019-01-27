#!/usr/bin/env python
# coding=utf-8

from logic import _logic_base
from config import db_config


class InfomationLogic(_logic_base.LogicBase):
    """信息管理表逻辑类"""

    def __init__(self):
        # 表名称
        self.__table_name = 'infomation'
        # 初始化
        _logic_base.LogicBase.__init__(self, db_config.DB, db_config.IS_OUTPUT_SQL, self.__table_name)