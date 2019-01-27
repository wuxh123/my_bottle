#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import db_helper
from common.string_helper import string
from config import db_config
from logic import product_logic, product_class_logic


class DbHelperTest(unittest.TestCase):
    """数据库操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        ##############################################
        # 只需要看这里，其他代码是测试用例的模板代码 #
        ##############################################
        # 测试事务
        # 使用with方法，初始化数据库链接
        with db_helper.PgHelper(db_config.DB, db_config.IS_OUTPUT_SQL) as db:
            # 实例化product表操作类ProductLogic
            _product_logic = product_logic.ProductLogic()
            # 实例化product_class表操作类product_class_logic
            _product_class_logic = product_class_logic.ProductClassLogic()
            # 初始化产品分类主键id
            id = 1

            # 获取产品分类信息（为了查看效果，所以加了这段获取分类信息）
            sql = _product_class_logic.get_model_for_pk_sql(id)
            print(sql)
            # 执行sql语句
            result = db.execute(sql)
            if not result:
                print('不存在指定的产品分类')
                return
            print('----产品分类实体----')
            print(result)
            print('-------------------')

            # 禁用产品分类
            fields = {
                'is_enable': 0
            }
            sql = _product_class_logic.edit_model_sql(id, fields, returning='is_enable')
            print(sql)
            # 执行sql语句
            result = db.execute(sql)
            if not result:
                # 执行失败，执行回滚操作
                db.rollback()
                print('禁用产品分类失败')
                return
            # 执行缓存清除操作
            _product_class_logic.del_model_for_cache(id)
            _product_class_logic.del_relevance_cache()
            print('----执行成功后的产品分类实体----')
            print(result)
            print('-------------------------------')

            # 同步禁用产品分类对应的所有产品
            sql = _product_logic.edit_sql(fields, 'product_class_id=' + str(id), returning='is_enable')
            print(sql)
            # 执行sql语句
            result = db.execute(sql)
            if not result:
                # 执行失败，执行回滚操作
                db.rollback()
                print('同步禁用产品分类对应的所有产品失败')
                return
            # 执行缓存清除操作
            for model in result:
                _product_class_logic.del_model_for_cache(model.get('id'))
            _product_class_logic.del_relevance_cache()
            print('----执行成功后的产品实体----')
            print(result)
            print('---------------------------')

            db.commit()
            print('执行成功')
        ##############################################

if __name__ == '__main__':
    unittest.main()
