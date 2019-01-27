#!/usr/bin/env python
# coding=utf-8

from logic import _logic_base
from config import db_config
from common import encrypt_helper, cache_helper


class MenuInfoLogic(_logic_base.LogicBase):
    """菜单管理表逻辑类"""

    def __init__(self):
        # 表名称
        self.__table_name = 'menu_info'
        # 初始化
        _logic_base.LogicBase.__init__(self, db_config.DB, db_config.IS_OUTPUT_SQL, self.__table_name)

    def get_model_for_url(self, key):
        """通过当前页面路由url，获取菜单对应的记录"""
        # 使用md5生成对应的缓存key值
        key_md5 = encrypt_helper.md5(key)
        # 从缓存中提取菜单记录
        model = cache_helper.get(key_md5)
        # 记录不存在时，运行记录载入缓存程序
        if not model:
            self._load_cache()
            model = cache_helper.get(key_md5)
        return model

    def _load_cache(self):
        """全表记录载入缓存"""
        # 生成缓存载入状态key，主要用于检查是否已执行了菜单表载入缓存判断
        cache_key = self.__table_name + '_is_load'
        # 将自定义的key存储到全局缓存队列中（关于全局缓存队列请查看前面ORM对应章节说明）
        self.add_relevance_cache_in_list(cache_key)
        # 获取缓存载入状态，检查记录是否已载入缓存，是的话则不再执行
        if cache_helper.get(cache_key):
            return
        # 从数据库中读取全部记录
        result = self.get_list()
        # 标记记录已载入缓存
        cache_helper.set(cache_key, True)
        # 如果菜单表没有记录，则直接退出
        if not result:
            return
        # 循环遍历所有记录，组合处理后，存储到nosql缓存中
        for model in result.get('rows', {}):
            # 提取菜单页面对应的接口（后台菜单管理中的接口值，同一个菜单操作时，经常需要访问多个接口，所以这个值有中存储多们接口值）
            interface_url = model.get('interface_url', '')
            if not interface_url:
                continue
            # 获取前端html页面地址
            page_url = model.get('page_url', '')

            # 同一页面接口可能有多个，所以需要进行分割
            interface_url_arr = interface_url.replace('\n', '').replace(' ', '').split(',')
            # 逐个接口处理
            for interface in interface_url_arr:
                # html+接口组合生成key
                url_md5 = encrypt_helper.md5(page_url + interface)
                # 存储到全局缓存队列中，方便菜单记录更改时，自动清除这些自定义缓存
                self.add_relevance_cache_in_list(url_md5)
                # 存储到nosql缓存
                cache_helper.set(url_md5, model)
