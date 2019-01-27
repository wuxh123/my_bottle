#!/usr/bin/evn python
# coding=utf-8

import unittest
from logic import manager_logic

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
        # 实例化manager表操作类ManagerLogic
        _manager_logic = manager_logic.ManagerLogic()
        # 执行get_model()方法，获取记录实体
        model = _manager_logic.get_model_for_pk(1)
        print(model)

        ##############################################

if __name__ == '__main__':
    unittest.main()
