#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : createconf.py
# @Author: xuxuedong
# @Date  : 2020/12/6
# @Desc

from jinja2 import PackageLoader, Environment, FileSystemLoader
import yaml,os



FILE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class CreateConf(object):

    def __init__(self,task):
        self.task = task
        self.get_config_for_rio()
    def get_config_for_rio(self):
        '''
        渲染配置文件
        :return:
        '''
        # 获取配置
        try:
            with open(f'{FILE_DIR}/task/{self.task}/config.yaml', encoding='UTF-8') as yaml_file:
                config = yaml.safe_load(yaml_file)

            # 获取配置模板
            env = Environment(loader=FileSystemLoader(searchpath=f"{FILE_DIR}task/{self.task}"))
            template = env.get_template(name='check_list.yaml.j2')

            # 渲染配置并生成配置文件
            real_config = template.render(config=config)
            f = open("{FILE_DIR}/task/rio/check_list.yaml", 'w', encoding="utf-8")
            f.write(real_config)
            f.close()
        except FileExistsError as e:
            print("Exception:",e)