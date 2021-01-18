#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : operations.py
# @Author: xuxuedong
# @Date  : 2020/11/30
# @Desc
from lib.SshHost import SSH
class SH(object):
    def exec_command(self,command,environment=None):
        pass

class LoginHost (object):
    def __init__(self,host_str):
        #解析host_str后返回[42.192.144.152,root,2007,36000] 对应ip , user , passwd , port
        self.ip,self.user,self.passwd,self.port = self._parsehost(host_str)
        # print(self.ip,self.user,self.passwd,self.port)
        if self.is_local(self.ip):
            self.operation = SH()
        else:
            #获取一个runner
            self.operation = SSH(hostname=self.ip, port=self.port, username=self.user, password=self.passwd)

    def conn_info(self):
        return {
            "HOST_USER": self.user,
            "HOST_IP":   self.ip,
            "HOST_PORT": self.port
        }
    def is_local(self, ip):
        """
        判断 runner 是否本地
        """
        return ip in ['localhost', '127.0.0.1']

    def _parsehost(self,host_str):
        '''
        :param host_str: ”42.192.144.152,root,Tcdn@2007,36000“ 将字符串进行解析
        :return: [42.192.144.152,root,2007,36000]
        '''
        host_str = str(host_str).strip()
        ip , user , passwd , port= host_str.split(",")
        return ip , user , passwd , port