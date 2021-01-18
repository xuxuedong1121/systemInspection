#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : untils.py
# @Author: xuxuedong
# @Date  : 2020/12/2
# @Desc
from functools import wraps
from core.log import str_color
import os,time,json
from datetime import datetime, date
from decimal import Decimal
SUCCESS_STATUS_CODE = 0
FAILED_STATUS_CODE = 1
WARN_STATUS_CODE = 2

STATUS_LIST= ["成功", "失败", "警告"]

SUCC_STR = str_color("green", STATUS_LIST[SUCCESS_STATUS_CODE])
FAIL_STR = str_color("red", STATUS_LIST[FAILED_STATUS_CODE])
WARN_STR = str_color("yellow", STATUS_LIST[WARN_STATUS_CODE])

def get_chinese_len(unicode_str):
    """包含中文字符串长度"""
    try:
        row_l = len(unicode_str)
        utf8_l = len(unicode_str.encode('utf-8'))
        return (utf8_l - row_l) / 2
    except Exception:
        return None


def exec_try_except(func):
    '''
    :param func:执行方法如mem_useage()并对此方法进行异常捕获返回异常防止程勋终止
    :return: 返回异常数据
    '''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            return 101, str(e)
    return wrapper

def check_task(task_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print("task_name:",task_name)
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            real_task_name = kwargs.pop("desc", None)
            real_task_name = task_name if real_task_name is None else real_task_name
            try:
                status, msg = func(self, *args, **kwargs)
            except Exception as e:
                # print(traceback.format_exc())
                status, msg = FAILED_STATUS_CODE, str(e)

            # console code
            if self.CONSOLE_CODE is None or self.CONSOLE_CODE == status:
                try:
                    self._task_index += 1
                except AttributeError:
                    setattr(self, "_task_index", 0)
                if status == SUCCESS_STATUS_CODE:
                    self.logger.info(u"|   |   |-- [{:>3}] {}  [{}]".format(self._task_index, "{:%s}" % int(
                        65 - get_chinese_len(real_task_name)), SUCC_STR).format(real_task_name))
                elif status == FAILED_STATUS_CODE:
                    self.logger.info(u"|   |   |-- [{:>3}] {}  [{}]".format(self._task_index, "{:%s}" % int(
                        65 - get_chinese_len(real_task_name)), FAIL_STR).format(real_task_name))
                elif status == WARN_STATUS_CODE:
                    self.logger.info(u"|   |   |-- [{:>3}] {}  [{}]".format(self._task_index, "{:%s}" % int(
                        65 - get_chinese_len(real_task_name)), WARN_STR).format(real_task_name))
            return {"name": real_task_name, "datetime": nowtime, "status": status, "msg": msg}

        wrapper.__setattr__("__is_check_task__", True)
        return wrapper

    return decorator


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")

        elif isinstance(o, bytes):
            return str(o, encoding="utf-8")

        elif isinstance(o, Decimal):
            return float(o)

        return json.JSONEncoder.default(self, o)