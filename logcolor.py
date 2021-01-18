#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : logcolor.py
# @Author: xuxuedong
# @Date  : 2020/11/27
# @Desc

colors = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'red': '\033[91m',
          'ENDC': '\033[0m', 'bold': '\033[1m', 'underline': '\033[4m'}

SUCCESS_STATUS_CODE = 0
FAILED_STATUS_CODE = 1
WARN_STATUS_CODE = 2
STATUS_LIST = ["成功", "失败", "警告"]

def str_color(color, data):
    return colors[color] + str(data) + colors['ENDC']
print(str_color("red", f'输入的数据不在巡检产品列表，请输入正确的产品名称，如：{STATUS_LIST[WARN_STATUS_CODE]}'))
sc = str_color("red", f'输入的数据不在巡检产品列表，请输入正确的产品名称，如：{STATUS_LIST[WARN_STATUS_CODE]}')

print(sc)

import functools

def add(a , b):
    print( a + b )

