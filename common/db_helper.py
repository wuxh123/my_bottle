#!/usr/bin/env python
# coding=utf-8

import psycopg2
import time
from io import StringIO
import sys
from common import log_helper


class PgHelper(object):
    """postgresql数据库操作类"""

    def __init__(self, db, is_output_sql):
        self.connect = None
        self.cursor = None
        # 初始化数据库参数
        self.db_name = db.get('db_name', '')
        self.db_user = db.get('db_user', '')
        self.db_pass = db.get('db_pass', '')
        self.db_host = db.get('db_host', '')
        self.db_port = db.get('db_port', '')
        # 是否将所有要执行的Sql语句输出到日志里
        self.is_output_sql = is_output_sql

    def open_conn(self):
        """连接数据库，并建立游标"""
        try:
            if not self.connect:
                self.connect = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass,
                                                host=self.db_host, port=self.db_port)
            return self.connect
        except Exception as e:
            log_helper.error('连接数据库失败：' + str(e.args))
            return False

    def close_conn(self):
        """关闭postgresql数据库链接"""
        # 关闭游标
        try:
            if self.cursor:
                self.cursor.close()
        except Exception:
            pass
        # 关闭数据库链接
        try:
            if self.connect:
                self.connect.close()
        except Exception:
            pass

    def __enter__(self):
        """初始化数据库链接"""
        self.open_conn()
        return self

    def __exit__(self, type, value, trace):
        """关闭postgresql数据库链接"""
        self.close_conn()

    def rollback(self):
        """回滚操作"""
        try:
            # 异常时，进行回滚操作
            if self.connect:
                self.connect.rollback()
        except Exception as e:
            log_helper.error('回滚操作失败：' + str(e.args))

    def commit(self):
        """提交事务"""
        try:
            if self.connect:
                self.connect.commit()
                self.close_conn()
        except Exception as e:
            log_helper.error('提交事务失败：' + str(e.args))

    def get_sql(self, query, vars=None):
        """获取编译后的sql语句"""
        # 记录程序执行开始时间
        start_time = time.process_time()
        try:
            # 判断是否记录sql执行语句
            if self.is_output_sql:
                log_helper.info('sql:' + str(query))
            # 建立游标
            self.cursor = self.connect.cursor()
            # 执行SQL
            self.data = self.cursor.mogrify(query, vars)
        except Exception as e:
            # 将异常写入到日志中
            log_helper.error('sql生成失败:' + str(e.args) + ' query:' + str(query))
            self.data = '获取编译sql失败'
        finally:
            # 关闭游标
            self.cursor.close()
        # 记录程序执行结束时间
        end_time = time.process_time()
        # 写入日志
        self.write_log(start_time, end_time, query)

        return self.data

    def copy(self, values, table_name, columns):
        """
        百万级数据更新函数
        :param values: 更新内容，字段之间用\t分隔，记录之间用\n分隔 "1\taaa\tabc\n2\bbb\abc\n"
        :param table_name: 要更新的表名称
        :param columns: 需要更新的字段名称：例：('id','userame','passwd')
        :return:
        """
        try:
            # 建立游标
            self.cursor = self.connect.cursor()
            self.cursor.copy_from(StringIO(values), table_name, columns=columns)
            self.connect.commit()
            return True
        except Exception as e:
            # 将异常写入到日志中
            log_helper.error('批量更新失败:' + str(e.args) + ' table:' + table_name)
        finally:
            # 关闭游标
            self.cursor.close()

    def execute(self, query, vars=None):
        """执行sql语句查询，返回结果集或影响行数"""
        if not query:
            return None
        # 记录程序执行开始时间
        start_time = time.process_time()
        try:
            # 判断是否记录sql执行语句
            if self.is_output_sql:
                log_helper.info('sql:' + str(query))
            # 建立游标
            self.cursor = self.connect.cursor()
            # 执行SQL
            result = self.cursor.execute(query, vars)
        except Exception as e:
            # 将异常写入到日志中
            log_helper.error('sql执行失败:' + str(e.args) + ' query:' + str(query))
            self.data = None
        else:
            # 获取数据
            try:
                if self.cursor.description:
                    # 在执行insert/update/delete等更新操作时，如果添加了returning，则读取返回数据组合成字典返回
                    self.data = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]
                else:
                    # 如果执行insert/update/delete等更新操作时没有添加returning，则返回影响行数，值为0时表时没有数据被更新
                    self.data = self.cursor.rowcount
            except Exception as e:
                # 将异常写入到日志中
                log_helper.error('数据获取失败:' + str(e.args) + ' query:' + str(query))
                self.data = None
        finally:
            # 关闭游标
            self.cursor.close()
        # 记录程序执行结束时间
        end_time = time.process_time()
        # 写入日志
        self.write_log(start_time, end_time, query)

        # 如果有返回数据，则把该数据返回给调用者
        return self.data


    def write_log(self, start_time, end_time, sql):
        """记录Sql执行超时日志"""
        t = end_time - start_time
        if (t) > 0.1:
            content = ' '.join(('run time:', str(t), 's sql:', sql))
            log_helper.info(content)

