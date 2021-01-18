#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : taskdata.py
# @Author: xuxuedong
# @Date  : 2020/11/28
# @Desc

import os,yaml
from lib.YAML import Yaml

#获取当前文件所在目录
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

class TasksData(object):
    '''
    从task中获取yaml配置文件数据
    ：__BASE_PATH__：为拼接task目录：/shell/systemInspection/core/../task
    '''
    __BASE_PATH__ = os.path.join(CURRENT_PATH, os.pardir, "task")
    def __init__(self,task):
        '''
        :param task: 传入-p中的参数mysql等
        :self.pathdir: 拼接获取运行任务所在目录如：/shell/systemInspection/core/../task/mysql
        :self.yamlmain：拼接获取运行巡检任务下的main.yaml如：/shell/systemInspection/core/../task/mysql/main.yaml
        :self._check(): 私有方法（函数）无法被外部调用，仅在实例化过程中进行实例参数自检
        '''
        # print(self.__BASE_PATH__)
        self.task = task
        self.pathdir = os.path.join(self.__BASE_PATH__,task)
        print( self.pathdir)
        self.yamlmain = os.path.join(self.pathdir,'main.yaml')
        self._check()

    def _check(self):
        '''
        实例自检方法，在初始化init时候判断是否有巡查任务所在目录，如果没有则抛出异常。
        同时判断任务目录中是否有main。yaml文件，如果没有抛出异常
        :return:
        '''
        if not os.path.exists(self.pathdir):
            raise Exception(f"{self.pathdir} isn't exists")
        if not os.path.exists(self.yamlmain):
            raise FileExistsError("main yaml isn't found under %s" %self.yamlmain)

    def _parseyaml(self,ydata):
        '''
        解析tasks中的数据及时解析check_list.yaml中的yaml数据并将
        :param ydata: 数据如：{'name': 'xxx 产品巡检', 'tasks': [{'include': 'check_list.yaml'}]}
        :return:'check_list.yaml'中yaml数据
        '''
        task_list = []
        for task in ydata["tasks"]:
            # print('task:',task)
            '''
            仅获取tasks中的数据并进行判断如果是字典类型包含include字段加载include字段
            中的yaml文件并将加载数据添加至task_list
            '''
            if isinstance(task, dict) and "include" in task:
                task_list += Yaml.load(os.path.join(self.pathdir, task["include"]))
            else:
                task_list.append(task)
        ydata["tasks"] = task_list
        return ydata

    def loadyaml(self):
        '''
        获取yamlmain中的yaml数据
        :return:返回数据如：{'name': 'xxx 产品巡检', 'tasks': [{'include': 'check_list.yaml'}]}
        '''
        # print(Yaml.load(self.yamlmain ))
        return Yaml.load(self.yamlmain)

    def get_taskdata(self):
        '''
        获取main.yaml中include中 xxx.yaml文件中所有的数据
        :return:
        '''
        return self._parseyaml(self.loadyaml())


