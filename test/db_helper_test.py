#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import db_helper
from config import db_config

class DbHelperTest(unittest.TestCase):
    """数据库操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        # 使用with方法，初始化数据库连接
        with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
            # 设置sql执行语句
            sql = """insert into product (name, code) values (%s, %s) returning id"""
            # 设置提交参数
            vars = ('张三', '201807251234568')
            # 生成sql语句，并打印到控制台
            print(db.get_sql(sql, vars))

            db.execute('select * from product where id=1000')
            db.execute('insert into product (name, code) values (%s, %s) returning id', ('张三', '201807251234568'))
            db.commit()

if __name__ == '__main__':
    unittest.main()
