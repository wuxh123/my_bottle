#!/usr/bin/env python
# coding=utf-8

from logic import _logic_base
from common import db_helper, convert_helper
from config import db_config


class DepartmentLogic(_logic_base.LogicBase):
    """部门管理表逻辑类"""

    def __init__(self):
        # 表名称
        self.__table_name = 'department'
        # 初始化
        _logic_base.LogicBase.__init__(self, db_config.DB, db_config.IS_OUTPUT_SQL, self.__table_name)


    def create_code(self, parent_code):
        """按规则生成权限组编码"""
        # 判断是否传入了父权限组编码
        if not parent_code:
            with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
                ### 执行sql，获取指定父权限组编号下面的子权限组中，最大的子权限组编号
                sql = 'select max(code) as code from %(table_name)s where parent_id = 0' %  {'table_name': self.__table_name}
                result = db.execute(sql)
                # 如果子权限组编号为NULL，则直接添加
                if not result or not result[0].get('code'):
                    return '01'
                else:
                    # 获取的权限组编号+1
                    code = str(convert_helper.to_int0(result[0].get('code', '')) + 1)
                    # 子权限组编号长度求余是否有余数，是则返回时前面加0
                    if len(code) % 2 == 1:
                        return '0' + code
                    else:
                        return code
        # 没有传入父权限组编码，则表示为一级权限组
        else:
            with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
                ### 执行sql，获取指定父权限组编号下面的子权限组中，最大的子权限组编号
                sql = "select max(code) as code from %(table_name)s " \
                      "where code like '%(parent_code1)s' and length(code) = length('%(parent_code)s') + 2" % \
                      {'table_name': self.__table_name, 'parent_code1': parent_code + '%', 'parent_code': parent_code}
                result = db.execute(sql)
                # 如果子权限组编号为NULL，则直接添加
                if not result or not result[0].get('code'):
                    return parent_code + '01'
                else:
                    # 获取的权限组编号+1
                    code = str(convert_helper.to_int0(result[0].get('code', '')) + 1)
                    # 子权限组编号长度求余是否有余数，是则返回时前面加0
                    if len(code) % 2 == 1:
                        return '0' + code
                    else:
                        return code