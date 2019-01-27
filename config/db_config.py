#!/usr/bin/env python
# coding=utf-8


### 数据库链接参数 ###
DB = {
    'db_host': '127.0.0.1',     # 数据库链接地址
    'db_port': 5432,             # 数据库端口
    'db_name': 'iot',     # 数据库名称
    'db_user': 'postgres',      # 数据库账号
    'db_pass': 'root'         # 数据库登录密码
}
# 是否输出执行的Sql语句到日志中
IS_OUTPUT_SQL = False
