#!/usr/bin/env python
# coding=utf-8

import json
from bottle import delete, get, post, put
from common import convert_helper, string_helper, web_helper, log_helper
from common.string_helper import string
from common.except_helper import exception_handling
from logic import menu_info_logic, positions_logic, _common_logic


@get('/api/main/menu_info/')
@exception_handling
def callback():
    """
    主页面获取菜单列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 获取当前用户权限
    session = web_helper.get_session()
    if session:
        _positions_logic = positions_logic.PositionsLogic()
        page_power = _positions_logic.get_page_power(session.get('positions_id'))
    else:
        page_power = ''
    if not page_power:
        return web_helper.return_msg(-404, '您的登录已超时，请重新登录')

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 读取记录
    result = _menu_info_logic.get_list('*', 'is_show and is_enabled', orderby='sort')
    if result:
        # 定义最终输出的html存储变量
        html = ''
        for model in result.get('rows'):
            # 检查是否有权限
            if ',' + str(model.get('id')) + ',' in page_power:
                # 提取出第一级菜单
                if model.get('parent_id') == 0:
                    # 添加一级菜单
                    temp = """
                    <dl id="menu-%(id)s">
                        <dt><i class="Hui-iconfont">%(icon)s</i> %(name)s<i class="Hui-iconfont menu_dropdown-arrow">&#xe6d5;</i></dt>
                        <dd>
                            <ul>
                    """ % {'id': model.get('id'), 'icon': model.get('icon'), 'name': model.get('name')}
                    html = html + temp

                    # 从所有菜单记录中提取当前一级菜单下的子菜单
                    for sub_model in result.get('rows'):
                        # 检查是否有权限
                        if ',' + str(sub_model.get('id')) + ',' in page_power:
                            # 如果父id等于当前一级菜单id，则为当前菜单的子菜单
                            if sub_model.get('parent_id') == model.get('id'):
                                temp = """
                                <li><a data-href="%(page_url)s" data-title="%(name)s" href="javascript:void(0)">%(name)s</a></li>
                            """ % {'page_url': sub_model.get('page_url'), 'name': sub_model.get('name')}
                                html = html + temp

                    # 闭合菜单html
                    temp = """
                            </ul>
                        </dd>
                    </dl>
                        """
                    html = html + temp

        return web_helper.return_msg(0, '成功', {'menu_html': html})
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/menu_info/')
@exception_handling
def callback():
    """
    获取列表数据
    """
    # 检查用户权限
    _common_logic.check_user_power()

    # 父id
    parent_id = convert_helper.to_int0(web_helper.get_query('nodeid', '', is_check_null=False))
    # 页面索引
    page_number = convert_helper.to_int1(web_helper.get_query('page', '', is_check_null=False))
    # 页面页码与显示记录数量
    page_size = convert_helper.to_int0(web_helper.get_query('rows', '', is_check_null=False))
    # 接收排序参数
    sidx = web_helper.get_query('sidx', '', is_check_null=False)
    sord = web_helper.get_query('sord', '', is_check_null=False)
    # 初始化排序字段
    order_by = 'sort asc'
    if sidx:
        order_by = sidx + ' ' + sord

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 读取记录
    wheres = 'parent_id=' + str(parent_id)
    result = _menu_info_logic.get_list('*', wheres, page_number, page_size, order_by)
    if result:
        return json.dumps(result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/menu_info/tree/')
@exception_handling
def callback():
    """
    获取列表数据（树列表）
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 读取记录
    result = _menu_info_logic.get_list('id, parent_id, name, not is_leaf as open', 'is_leaf=false', orderby='sort asc')
    if result:
        return web_helper.return_msg(0, "成功", {'tree_list': result.get('rows')})
    else:
        return web_helper.return_msg(-1, "查询失败")


@get('/api/system/menu_info/positions/<id:int>/')
@exception_handling
def callback(id):
    """
    根据用户职位权限获取列表数据（树列表），为已有权限的数据赋值
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 读取记录（ztree控件需要输出记录id、父id、树节点名称、节点是否扩展和是否打勾这几项参数）
    result = _menu_info_logic.get_list('id, parent_id, name, not is_leaf as open, false as checked')
    if result and result.get('rows'):
        # 获取指定的职位记录
        _positions_logic = positions_logic.PositionsLogic()
        positions_logic_model = _positions_logic.get_model_for_cache(id)
        if positions_logic_model:
            # 读取该职位权限字串
            page_power = positions_logic_model.get('page_power', '')
            # 判断当前菜单项id是否存在于该职位的权限字串中
            for model in result.get('rows'):
                # 如果存在，则表示当前职位拥有该菜单项的权限，即在菜单权限列表中需要打勾
                if ',' + str(model.get('id', 0)) + ',' in page_power:
                    model['checked'] = True

        return web_helper.return_msg(0, "成功", {'tree_list': result.get('rows')})
    else:
        return web_helper.return_msg(-1, "查询失败")
    
    
@get('/api/system/menu_info/<id:int>/')
@exception_handling
def callback(id):
    """
    获取指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 读取记录
    result = _menu_info_logic.get_model_for_cache(id)
    if result:
        return web_helper.return_msg(0, '成功', result)
    else:
        return web_helper.return_msg(-1, "查询失败")


@post('/api/system/menu_info/')
@exception_handling
def callback():
    """
    新增记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '菜单名称')
    icon = web_helper.get_form('icon', '菜单小图标', True, 10, False, is_check_special_char=False)
    icon = icon.replace('\'', '').replace('|', '').replace('%', '')
    page_url = web_helper.get_form('page_url', '页面URL', is_check_null=False)
    interface_url = web_helper.get_form('interface_url', '接口url', is_check_null=False, is_check_special_char=False)
    # 替换编码
    interface_url = interface_url.replace('@', '').replace('\'', '').replace('|', '').replace('%', '')
    parent_id = convert_helper.to_int0(web_helper.get_form('parent_id', '父id', is_check_null=False))
    sort = convert_helper.to_int0(web_helper.get_form('sort', '排序', is_check_null=False))
    is_leaf = web_helper.get_form('is_leaf', '是否最终节点', is_check_null=False)
    is_show = web_helper.get_form('is_show', '是否显示', is_check_null=False)
    is_enabled = web_helper.get_form('is_enabled', '是否启用', is_check_null=False)

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 计算深度级别，即当前菜单在哪一级
    if parent_id == 0:
        level = 0
    else:
        level = _menu_info_logic.get_value_for_cache(parent_id, 'level') + 1
    # 如果没有设置排序，则自动获取当前级别最大的序号加1
    if sort == 0:
        sort = _menu_info_logic.get_max('sort', 'parent_id=' + str(parent_id)) + 1

    # 组合更新字段
    fields = {
        'name': string(name),
        'icon': string(icon),
        'page_url': string(page_url),
        'interface_url': string(interface_url),
        'parent_id': parent_id,
        'sort': sort,
        'level': level,
        'is_leaf': is_leaf,
        'is_show': is_show,
        'is_enabled': is_enabled,
    }
    # 新增记录
    result = _menu_info_logic.add_model(fields)
    if result:
        return web_helper.return_msg(0, '提交成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@put('/api/system/menu_info/<id:int>/')
@exception_handling
def callback(id):
    """
    修改记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    name = web_helper.get_form('name', '菜单名称')
    icon = web_helper.get_form('icon', '菜单小图标', True, 10, False, is_check_special_char=False)
    icon = icon.replace('\'', '').replace('|', '').replace('%', '')
    page_url = web_helper.get_form('page_url', '页面URL', is_check_null=False)
    interface_url = web_helper.get_form('interface_url', '接口url', is_check_null=False, is_check_special_char=False)
    # 替换编码
    interface_url = interface_url.replace('\'', '').replace('|', '').replace('%', '')
    parent_id = convert_helper.to_int0(web_helper.get_form('parent_id', '父id', is_check_null=False))
    sort = convert_helper.to_int0(web_helper.get_form('sort', '排序', is_check_null=False))
    is_leaf = web_helper.get_form('is_leaf', '是否最终节点', is_check_null=False)
    is_show = web_helper.get_form('is_show', '是否显示', is_check_null=False)
    is_enabled = web_helper.get_form('is_enabled', '是否启用', is_check_null=False)

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 如果没有设置排序，则自动获取当前级别最大的序号加1
    if sort == 0:
        sort = _menu_info_logic.get_max('sort', 'parent_id=' + str(parent_id)) + 1

    # 组合更新字段
    fields = {
        'name': string(name),
        'icon': string(icon),
        'page_url': string(page_url),
        'interface_url': string(interface_url),
        'sort': sort,
        'is_leaf': is_leaf,
        'is_show': is_show,
        'is_enabled': is_enabled,
    }
    # 修改记录
    result = _menu_info_logic.edit_model(id, fields)
    if result:
        return web_helper.return_msg(0, '提交成功')
    else:
        return web_helper.return_msg(-1, "提交失败")


@delete('/api/system/menu_info/<id:int>/')
@exception_handling
def callback(id):
    """
    删除指定记录
    """
    # 检查用户权限
    _common_logic.check_user_power()

    _menu_info_logic = menu_info_logic.MenuInfoLogic()
    # 判断要删除的节点是否有子节点，是的话不能删除
    if _menu_info_logic.exists('parent_id=' + str(id)):
        return web_helper.return_msg(-1, "当前菜单存在子菜单，不能直接删除")

    # 删除记录
    result = _menu_info_logic.delete_model(id)
    if result:
        return web_helper.return_msg(0, '删除成功')
    else:
        return web_helper.return_msg(-1, "删除失败")
