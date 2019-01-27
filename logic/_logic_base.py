#!/usr/bin/env python
# coding=utf-8

from common import db_helper, cache_helper, encrypt_helper


class LogicBase():
    """逻辑层基础类"""

    def __init__(self, db, is_output_sql, table_name, column_name_list='*', pk_name='id'):
        """类初始化"""
        # 数据库参数
        self.__db = db
        # 是否输出执行的Sql语句到日志中
        self.__is_output_sql = is_output_sql
        # 表名称
        self.__table_name = str(table_name).lower()
        # 查询的列字段名称，*表示查询全部字段，多于1个字段时用逗号进行分隔，除了字段名外，也可以是表达式
        self.__column_name_list = str(column_name_list).lower()
        # 主健名称
        self.__pk_name = str(pk_name).lower()
        # 缓存列表
        self.__cache_list = self.__table_name + '_cache_list'

    #####################################################################
    ### 生成Sql ###
    def get_model_sql(self, wheres):
        """通过条件获取一条记录"""
        # 如果有条件，则自动添加where
        if wheres:
            wheres = ' where ' + wheres

        # 合成sql语句
        sql = "select %(column_name_list)s from %(table_name)s %(wheres)s" % \
              {'column_name_list': self.__column_name_list, 'table_name': self.__table_name, 'wheres': wheres}
        return sql

    def get_model_for_pk_sql(self, pk, wheres=''):
        """通过主键值获取数据库记录实体"""
        # 组装查询条件
        wheres = '%s = %s' % (self.__pk_name, str(pk))
        return self.get_model_sql(wheres)

    def get_value_sql(self, column_name, wheres=''):
        """
        获取指定条件的字段值————多于条记录时，只取第一条记录
        :param column_name: 单个字段名，如：id
        :param wheres: 查询条件
        :return: 7 （指定的字段值）
        """
        if wheres:
            wheres = ' where ' + wheres

        sql = 'select %(column_name)s from %(table_name)s %(wheres)s limit 1' % \
              {'column_name': column_name, 'table_name': self.__table_name, 'wheres': wheres}
        return sql

    def get_value_list_sql(self, column_name, wheres=''):
        """
        获取指定条件记录的字段值列表
        :param column_name: 单个字段名，如：id
        :param wheres: 查询条件
        :return: [1,3,4,6,7]
        """
        if not column_name:
            column_name = self.__pk_name
        elif wheres:
            wheres = ' where ' + wheres

        sql = 'select array_agg(%(column_name)s) as list from %(table_name)s %(wheres)s' % \
              {'column_name': column_name, 'table_name': self.__table_name, 'wheres': wheres}
        return sql

    def add_model_sql(self, fields, returning=''):
        """新增数据库记录"""
        ### 拼接sql语句 ###
        # 初始化变量
        key_list = []
        value_list = []
        # 将传入的字典参数进行处理，把字段名生成sql插入字段名数组和字典替换数组
        # PS:字符串使用字典替换参数时，格式是%(name)s，这里会生成对应的字串
        # 比如：
        #   传入的字典为： {'id': 1, 'name': '名称'}
        #   那么生成的key_list为：'id','name'
        #   而value_list为：'%(id)s,%(name)s'
        #   最终而value_list为字符串对应名称位置会被替换成相应的值
        for key in fields.keys():
            key_list.append(key)
            value_list.append('%(' + key + ')s')
        # 设置sql拼接字典，并将数组（lit）使用join方式进行拼接，生成用逗号分隔的字符串
        parameter = {
            'table_name': self.__table_name,
            'pk_name': self.__pk_name,
            'key_list': ','.join(key_list),
            'value_list': ','.join(value_list)
        }
        # 如果有指定返回参数，则添加
        if returning:
            parameter['returning'] = ', ' + returning
        else:
            parameter['returning'] = ''

        # 生成可以使用字典替换的字符串
        sql = "insert into %(table_name)s (%(key_list)s) values (%(value_list)s) returning %(pk_name)s %(returning)s" % parameter
        # 将生成好的字符串替字典参数值，生成最终可执行的sql语句
        return sql % fields

    def edit_sql(self, fields, wheres='', returning=''):
        """
        批量编辑数据库记录
        :param fields: 要更新的字段（字段名与值存储在字典中）
        :param wheres: 更新条件
        :param returning: 更新成功后，返回的字段名
        :param is_update_cache: 是否同步更新缓存
        :return:
        """
        ### 拼接sql语句 ###
        # 拼接字段与值
        field_list = [key + ' = %(' + key + ')s' for key in fields.keys()]
        # 设置sql拼接字典
        parameter = {
            'table_name': self.__table_name,
            'pk_name': self.__pk_name,
            'field_list': ','.join(field_list)
        }
        # 如果存在更新条件，则将条件添加到sql拼接更换字典中
        if wheres:
            parameter['wheres'] = ' where ' + wheres
        else:
            parameter['wheres'] = ''

        # 如果有指定返回参数，则添加
        if returning:
            parameter['returning'] = ', ' + returning
        else:
            parameter['returning'] = ''

        # 生成sql语句
        sql = "update %(table_name)s set %(field_list)s %(wheres)s returning %(pk_name)s %(returning)s" % parameter
        return sql % fields

    def edit_model_sql(self, pk, fields, wheres='', returning=''):
        """编辑单条数据库记录"""
        if wheres:
            wheres = self.__pk_name + ' = ' + str(pk) + ' and ' + wheres
        else:
            wheres = self.__pk_name + ' = ' + str(pk)

        return self.edit_sql(fields, wheres, returning)

    def delete_sql(self, wheres='', returning=''):
        """
        批量删除数据库记录
        :param wheres: 删除条件
        :param returning: 删除成功后，返回的字段名
        :param is_update_cache: 是否同步更新缓存
        :return:
        """
        # 如果存在条件
        if wheres:
            wheres = ' where ' + wheres

        # 如果有指定返回参数，则添加
        if returning:
            returning = ', ' + returning

        # 生成sql语句
        sql = "delete from %(table_name)s %(wheres)s returning %(pk_name)s %(returning)s" % \
              {'table_name': self.__table_name, 'wheres': wheres, 'pk_name': self.__pk_name, 'returning': returning}
        return sql

    def delete_model_sql(self, pk, wheres='', returning=''):
        """删除单条数据库记录"""
        if wheres:
            wheres = self.__pk_name + ' = ' + str(pk) + ' and ' + wheres
        else:
            wheres = self.__pk_name + ' = ' + str(pk)

        return self.delete_sql(wheres, returning)

    def get_list_sql(self, column_name_list='', wheres='', orderby=None, table_name=None):
        """
        获取指定条件的数据库记录集
        :param column_name_list:      查询字段
        :param wheres:      查询条件
        :param orderby:     排序规则
        :param table_name:     查询数据表，多表查询时需要设置
        :return:
        """
        # 初始化查询数据表名称
        if not table_name:
            table_name = self.__table_name
        # 初始化查询字段名
        if not column_name_list:
            column_name_list = self.__column_name_list
        # 初始化查询条件
        if wheres:
            # 如果是字符串，表示该查询条件已组装好了，直接可以使用
            if isinstance(wheres, str):
                wheres = 'where ' + wheres
            # 如果是list，则表示查询条件有多个，可以使用join将它们用and方式组合起来使用
            elif isinstance(wheres, list):
                wheres = 'where ' + ' and '.join(wheres)
        # 初始化排序
        if not orderby:
            orderby = self.__pk_name + ' desc'
        #############################################################

        ### 按条件查询数据库记录
        sql = "select %(column_name_list)s from %(table_name)s %(wheres)s order by %(orderby)s " % \
              {'column_name_list': column_name_list,
               'table_name': table_name,
               'wheres': wheres,
               'orderby': orderby}
        return sql

    def get_count_sql(self, wheres=''):
        """获取指定条件记录数量"""
        if wheres:
            wheres = ' where ' + wheres
        sql = 'select count(1) as total from %(table_name)s %(wheres)s ' % \
              {'table_name': self.__table_name, 'wheres': wheres}
        return sql

    def get_sum_sql(self, fields, wheres):
        """获取指定条件记录数量"""
        sql = 'select sum(%(fields)s) as total from %(table_name)s where %(wheres)s ' % \
              {'table_name': self.__table_name, 'wheres': wheres, 'fields': fields}
        return sql

    def get_min_sql(self, fields, wheres):
        """获取该列记录最小值"""
        sql = 'select min(%(fields)s) as min from %(table_name)s where %(wheres)s ' % \
              {'table_name': self.__table_name, 'wheres': wheres, 'fields': fields}
        return sql

    def get_max_sql(self, fields, wheres):
        """获取该列记录最大值"""
        sql = 'select max(%(fields)s) as max from %(table_name)s where %(wheres)s ' % \
              {'table_name': self.__table_name, 'wheres': wheres, 'fields': fields}
        return sql

    #####################################################################


    #####################################################################
    ### 执行Sql ###

    def select(self, sql):
        """执行sql查询语句（select）"""
        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            # 执行sql语句
            result = db.execute(sql)
            if not result:
                result = []
        return result

    def execute(self, sql):
        """执行sql语句，并提交事务"""
        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            # 执行sql语句
            result = db.execute(sql)
            if result:
                db.commit()
            else:
                result = []
        return result

    def copy(self, values, columns):
        """批量更新数据"""
        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            # 执行sql语句
            result = db.copy(values, self.__table_name, columns)
        return result

    def get_model(self, wheres):
        """通过条件获取一条记录"""
        # 生成sql
        sql = self.get_model_sql(wheres)
        # 执行查询操作
        result = self.select(sql)
        if result:
            return result[0]
        return {}

    def get_model_for_pk(self, pk, wheres=''):
        """通过主键值获取数据库记录实体"""
        if not pk:
            return {}
        # 生成sql
        sql = self.get_model_for_pk_sql(pk, wheres)
        # 执行查询操作
        result = self.select(sql)
        if result:
            return result[0]
        return {}

    def get_value(self, column_name, wheres=''):
        """
        获取指定条件的字段值————多于条记录时，只取第一条记录
        :param column_name: 单个字段名，如：id
        :param wheres: 查询条件
        :return: 7 （指定的字段值）
        """
        if not column_name:
            return None

        # 生成sql
        sql = self.get_value_sql(column_name, wheres)
        result = self.select(sql)
        # 如果查询成功，则直接返回记录字典
        if result:
            return result[0].get(column_name)

    def get_value_list(self, column_name, wheres=''):
        """
        获取指定条件记录的字段值列表
        :param column_name: 单个字段名，如：id
        :param wheres: 查询条件
        :return: [1,3,4,6,7]
        """
        # 生成sql
        sql = self.get_value_list_sql(column_name, wheres)
        result = self.select(sql)
        # 如果查询失败或不存在指定条件记录，则直接返回初始值
        if result and isinstance(result, list):
            return result[0].get('list')
        else:
            return []

    def add_model(self, fields, returning=''):
        """新增数据库记录"""
        # 生成sql
        sql = self.add_model_sql(fields, returning)
        result = self.execute(sql)
        if result:
            return result[0]
        return {}

    def edit(self, fields, wheres='', returning='', is_update_cache=True):
        """
        批量编辑数据库记录
        :param fields: 要更新的字段（字段名与值存储在字典中）
        :param wheres: 更新条件
        :param returning: 更新成功后，返回的字段名
        :param is_update_cache: 是否同步更新缓存
        :return:
        """
        # 生成sql
        sql = self.edit_sql(fields, wheres, returning)
        result = self.execute(sql)
        if result:
            # 判断是否删除对应的缓存
            if is_update_cache:
                # 循环删除更新成功的所有记录对应的缓存
                for model in result:
                    self.del_model_for_cache(model.get(self.__pk_name, 0))
                # 同步删除与本表关联的缓存
                self.del_relevance_cache()
        return result

    def edit_model(self, pk, fields, wheres='', returning='', is_update_cache=True):
        """编辑单条数据库记录"""
        if not pk:
            return {}
        # 生成sql
        sql = self.edit_model_sql(pk, fields, wheres, returning)
        result = self.execute(sql)
        if result:
            # 判断是否删除对应的缓存
            if is_update_cache:
                # 删除更新成功的所有记录对应的缓存
                self.del_model_for_cache(result[0].get(self.__pk_name, 0))
                # 同步删除与本表关联的缓存
                self.del_relevance_cache()
        return result

    def delete(self, wheres='', returning='', is_update_cache=True):
        """
        批量删除数据库记录
        :param wheres: 删除条件
        :param returning: 删除成功后，返回的字段名
        :param is_update_cache: 是否同步更新缓存
        :return:
        """
        # 生成sql
        sql = self.delete_sql(wheres, returning)
        result = self.execute(sql)
        if result:
            # 同步删除对应的缓存
            if is_update_cache:
                for model in result:
                    self.del_model_for_cache(model.get(self.__pk_name, 0))
                # 同步删除与本表关联的缓存
                self.del_relevance_cache()
        return result

    def delete_model(self, pk, wheres='', returning='', is_update_cache=True):
        """删除单条数据库记录"""
        if not pk:
            return {}
        # 生成sql
        sql = self.delete_model_sql(pk, wheres, returning)
        result = self.execute(sql)
        if result:
            # 同步删除对应的缓存
            if is_update_cache:
                self.del_model_for_cache(result[0].get(self.__pk_name, 0))
                # 同步删除与本表关联的缓存
                self.del_relevance_cache()
        return result

    def get_list(self, column_name_list='', wheres='', page_number=None, page_size=None, orderby=None, table_name=None):
        """
        获取指定条件的数据库记录集
        :param column_name_list:      查询字段
        :param wheres:      查询条件
        :param page_number:   分页索引值
        :param page_size:    分页大小， 存在值时才会执行分页
        :param orderby:     排序规则
        :param table_name:     查询数据表，多表查询时需要设置
        :return: 返回记录集总数量与分页记录集
            {'records': 0, 'total': 0, 'page': 0, 'rows': []}
        """
        # 初始化输出参数：总记录数量与列表集
        data = {
            'records': 0,  # 总记录数
            'total': 0,  # 总页数
            'page': 1,  # 当前页面索引
            'rows': [],  # 查询结果（记录列表）
        }
        # 初始化查询数据表名称
        if not table_name:
            table_name = self.__table_name
        # 初始化查询字段名
        if not column_name_list:
            column_name_list = self.__column_name_list
        # 初始化查询条件
        if wheres:
            # 如果是字符串，表示该查询条件已组装好了，直接可以使用
            if isinstance(wheres, str):
                wheres = 'where ' + wheres
            # 如果是list，则表示查询条件有多个，可以使用join将它们用and方式组合起来使用
            elif isinstance(wheres, list):
                wheres = 'where ' + ' and '.join(wheres)
        elif isinstance(wheres, list):
            wheres = ''
        # 初始化排序
        if not orderby:
            orderby = self.__pk_name + ' desc'
        # 初始化分页查询的记录区间
        paging = ''

        with db_helper.PgHelper(self.__db, self.__is_output_sql) as db:
            #############################################################
            # 判断是否需要进行分页
            if not page_size is None:
                ### 执行sql，获取指定条件的记录总数量
                sql = 'select count(1) as records from %(table_name)s %(wheres)s ' % \
                      {'table_name': table_name, 'wheres': wheres}
                result = db.execute(sql)
                # 如果查询失败或不存在指定条件记录，则直接返回初始值
                if not result or result[0]['records'] == 0:
                    return data

                # 设置记录总数量
                data['records'] = result[0].get('records')

                #########################################################
                ### 设置分页索引与页面大小 ###
                if page_size <= 0:
                    page_size = 10
                # 计算总分页数量：通过总记录数除于每页显示数量来计算总分页数量
                if data['records'] % page_size == 0:
                    page_total = data['records'] // page_size
                else:
                    page_total = data['records'] // page_size + 1
                # 判断页码是否超出限制，超出限制查询时会出现异常，所以将页面索引设置为最后一页
                if page_number < 1 or page_number > page_total:
                    page_number = page_total
                # 记录总页面数量
                data['total'] = page_total
                # 记录当前页面值
                data['page'] = page_number
                # 计算当前页面要显示的记录起始位置（limit指定的位置）
                record_number = (page_number - 1) * page_size
                # 设置查询分页条件
                paging = ' limit ' + str(page_size) + ' offset ' + str(record_number)
            #############################################################

            ### 按条件查询数据库记录
            sql = "select %(column_name_list)s from %(table_name)s %(wheres)s order by %(orderby)s %(paging)s" % \
                  {'column_name_list': column_name_list,
                   'table_name': table_name,
                   'wheres': wheres,
                   'orderby': orderby,
                   'paging': paging}
            result = db.execute(sql)
            if result:
                data['rows'] = result
                # 不需要分页查询时，直接在这里设置总记录数
                if page_size is None:
                    data['records'] = len(result)

        return data

    def get_count(self, wheres=''):
        """获取指定条件记录数量"""
        # 生成sql
        sql = self.get_count_sql(wheres)
        result = self.select(sql)
        # 如果查询存在记录，则返回true
        if result:
            return result[0].get('total')
        return 0

    def get_sum(self, fields, wheres):
        """获取指定条件记录数量"""
        # 生成sql
        sql = self.get_sum_sql(fields, wheres)
        result = self.select(sql)
        # 如果查询存在记录，则返回true
        if result and result[0].get('total'):
            return result[0].get('total')
        return 0

    def get_min(self, fields, wheres):
        """获取该列记录最小值"""
        # 生成sql
        sql = self.get_min_sql(fields, wheres)
        result = self.select(sql)
        # 如果查询存在记录，则返回true
        if result and result[0].get('min'):
            return result[0].get('min')
        return 0

    def get_max(self, fields, wheres):
        """获取该列记录最大值"""
        # 生成sql
        sql = self.get_max_sql(fields, wheres)
        result = self.select(sql)
        # 如果查询存在记录，则返回true
        if result and result[0].get('max'):
            return result[0].get('max')
        return 0

    def exists(self, wheres):
        """检查指定条件的记录是否存在"""
        return self.get_count(wheres) > 0

    #####################################################################


    #####################################################################
    ### 缓存操作方法 ###

    def get_cache_key(self, pk):
        """获取缓存key值"""
        return ''.join((self.__table_name, '_', str(pk)))

    def set_model_for_cache(self, pk, value, time=43200):
        """更新存储在缓存中的数据库记录，缓存过期时间为12小时"""
        # 生成缓存key
        key = self.get_cache_key(pk)
        # 存储到nosql缓存中
        cache_helper.set(key, value, time)

    def get_model_for_cache(self, pk):
        """从缓存中读取数据库记录"""
        # 生成缓存key
        key = self.get_cache_key(pk)
        # 从缓存中读取数据库记录
        result = cache_helper.get(key)
        # 缓存中不存在记录，则从数据库获取
        if not result:
            result = self.get_model_for_pk(pk)
            self.set_model_for_cache(pk, result)
        if result:
            return result
        else:
            return {}

    def get_model_for_cache_of_where(self, where):
        """
        通过条件获取记录实体——条件必须是额外的主键，也就是说记录是唯一的（我们经常需要使用key、编码或指定条件来获取记录，这时可以通过当前方法来获取）
        :param where: 查询条件
        :return: 记录实体
        """
        # 生成实体缓存key
        model_cache_key = self.__table_name + encrypt_helper.md5(where)
        # 通过条件从缓存中获取记录id
        pk = cache_helper.get(model_cache_key)
        # 如果主键id存在，则直接从缓存中读取记录
        if pk:
            return self.get_model_for_cache(pk)

        # 否则从数据库中获取
        result = self.get_model(where)
        if result:
            # 存储条件对应的主键id值到缓存中
            cache_helper.set(model_cache_key, result.get(self.__pk_name))
            # 存储记录实体到缓存中
            self.set_model_for_cache(result.get(self.__pk_name), result)
            return result

    def get_value_for_cache(self, pk, column_name):
        """获取指定记录的字段值"""
        return self.get_model_for_cache(pk).get(column_name)

    def del_model_for_cache(self, pk):
        """删除缓存中指定数据"""
        # 生成缓存key
        key = self.get_cache_key(pk)
        # log_helper.info(key)
        # 存储到nosql缓存中
        cache_helper.delete(key)

    def add_relevance_cache_in_list(self, key):
        """将缓存名称存储到列表里————主要存储与记录变更关联的"""
        # 从nosql中读取全局缓存列表
        cache_list = cache_helper.get(self.__cache_list)
        # 判断缓存列表是否有值，有则进行添加操作
        if cache_list:
            # 判断是否已存储列表中，不存在则执行添加操作
            if not key in cache_list:
                cache_list.append(key)
                cache_helper.set(self.__cache_list, cache_list)
        # 无则直接创建全局缓存列表，并存储到nosql中
        else:
            cache_list = [key]
            cache_helper.set(self.__cache_list, cache_list)

    def del_relevance_cache(self):
        """删除关联缓存————将和数据表记录关联的，个性化缓存全部删除"""
        # 从nosql中读取全局缓存列表
        cache_list = cache_helper.get(self.__cache_list)
        # 清除已删除缓存列表
        cache_helper.delete(self.__cache_list)
        if cache_list:
            # 执行删除操作
            for cache in cache_list:
                cache_helper.delete(cache)

    #####################################################################
