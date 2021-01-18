#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : YAML.py
# @Author: xuxuedong
# @Date  : 2020/11/29
# @Desc
import yaml

class Yaml(object):

    def __init__(self, yarml_file):
        self.yarml_file = yarml_file

    def read(self):
        with open(self.yarml_file,'r',encoding='utf-8') as yf:
            return yaml.load(yf,Loader=yaml.FullLoader)
    def write(self,data):
        with open(self.yarml_file,'w',encoding='utf-8') as yf:
            return yaml.dump(data,yf,Dumper=yaml.SafeDumper)
    @staticmethod
    def load(yaml_file):
        with open(yaml_file,'r',encoding='utf-8') as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)