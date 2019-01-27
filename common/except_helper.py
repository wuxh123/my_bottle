#!/usr/bin/env python
# coding=utf-8

import os
import sys
from bottle import HTTPResponse
from common import log_helper, web_helper


def detailtrace():
    """获取程序当前运行的堆栈信息"""
    retStr = ""
    f = sys._getframe()
    f = f.f_back  # first frame is detailtrace, ignore it
    while hasattr(f, "f_code"):
        co = f.f_code
        retStr = "%s(%s:%s)->" % (os.path.basename(co.co_filename),
                                  co.co_name,
                                  f.f_lineno) + retStr
        f = f.f_back
    return retStr


def exception_handling(func):
    """接口异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            # 执行接口方法
            return func(*args, **kwargs)
        except Exception as e:
            # 捕捉异常，如果是中断无返回类型操作，则再执行一次
            if isinstance(e, HTTPResponse):
                func(*args, **kwargs)
            # 否则写入异常日志，并返回错误提示
            else:
                log_helper.error(str(e.args))
                return web_helper.return_msg(-1, "操作失败")
    return wrapper
