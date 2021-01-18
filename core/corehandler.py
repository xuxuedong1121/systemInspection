#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : corehandler.py
# @Author: xuxuedong
# @Date  : 2020/11/30
# @Desc
import inspect
import six,abc

from pike.manager import PikeManager
from core.operations import LoginHost
import os
from functools import partial
from lib.untils import *

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
PLUGINS_DIR = os.path.join(CURRENT_PATH,os.pardir,'plugins')
# @six.add_metaclass(abc.ABCMeta)
class HealthCheck(object):

    role = ""
    subject_name = ""

    # consule 展示指定状态码巡检项
    CONSOLE_CODE = None

    SUCCESS_STATUS_CODE = SUCCESS_STATUS_CODE
    FAILED_STATUS_CODE = FAILED_STATUS_CODE
    WARN_STATUS_CODE = WARN_STATUS_CODE
    # 插件runner, 在插件实例化时根据hosts分配的默认runner
    runner = None

    def __init__(self,runner):
        runner.operation.exec_command = partial(runner.operation.exec_command, environment=runner.conn_info())
        self.runner = runner
    @staticmethod
    def get_plugins():
        '''
        采用插件管理器pike将插件目录（PLUGINS_DIR）传入后获取$PLUGINS_DIR中所有的类，并将其变成dic；
        x.role为插件(class中的role属性)中的role名循环赋值获取插件类。
        :return:{'host-system': <class 'host-system.SystemCheck'>,'mysql-system':<class 'mysql-system.MysqlCheck'>}
        '''
        with PikeManager([PLUGINS_DIR]) as mgplugin:
            return {x.role: x for x in mgplugin.get_classes() if x.__base__.__name__ == "HealthCheck" }

    def _run(self, funcs):
        '''
        :param funcs: [{'func': 'mem_useage'}, {'func': 'load_average', 'desc': '检查最近5分钟系统平均负载是否小于CPU核数', 'args': {'N': 5}}, {'
func': 'sync_date'}, {'func': 'ping'}, {'func': 'ping_delay', 'desc': 'ping网络延迟小于 1 ms', 'args': {'max_ms': 1}}, {'func': 'partition_useage', 'desc':
'检查挂载点 / 使用率小于80%', 'args': {'mountpoint': '/'}}, {'func': 'partition_useage', 'desc': '检查挂载点 /data 使用率小于80%', 'args': {'mountpoint': '/
data'}}]}]
        funcs_dic: 解析本插件中的所有方法转成dic
        :return:
        '''
        # print("self",dir(self))
        funcs_dic = {x.__name__: x for x in [getattr(self,attr) for attr in dir(self)]
                     if inspect.ismethod(x)}
        # print(funcs_dic)
        if funcs is None or (isinstance(funcs,list) and len(funcs) == 0):
            print("[m() for _, m in funcs_dic.items()]",[m() for _, m in funcs_dic.items()])
            return [m() for _, m in funcs_dic.items()]
        else:
            '''
            从funcs中提取func方法（因plugins中类的方法对应的是funcs中的值）
            '''
            rets = []
            for f in funcs:
                # print(f)
                #获取插件中执行任务方法
                method = funcs_dic.get(f["func"])
                desc = f.get("desc") or None
                args = f.get("args") or {}
                if method:
                    #将方法执行后的结果数据append至rets中，metho（**args）为执行方法
                    rets.append(method(**args,desc=desc))
            # print(rets)
            return rets

    def __call__(self, funcs):
        '''
        :param funcs:task任务中{'name': '操作系统 基础巡检', 'hosts': ['192.168.1.1,root,P@ssw0rd,36000', '192.168.1.2,root,P@ssw0rd,36000', '192.168.1.3,root,P@ssw0rd,36000'], 'roles': [
{'role': 'host-system', 'funcs': [{'func': 'mem_useage'}, {'func': 'load_average', 'desc': '检查最近5分钟系统平均负载是否小于CPU核数', 'args': {'N': 5}}, {'
func': 'sync_date'}, {'func': 'ping'}, {'func': 'ping_delay', 'desc': 'ping网络延迟小于 1 ms', 'args': {'max_ms': 1}}, {'func': 'partition_useage', 'desc':
'检查挂载点 / 使用率小于80%', 'args': {'mountpoint': '/'}}, {'func': 'partition_useage', 'desc': '检查挂载点 /data 使用率小于80%', 'args': {'mountpoint': '/
data'}}]}]}  roles中role为插件名，funcs为插件中的方法。
        :return:
        '''
        return self._run(funcs)