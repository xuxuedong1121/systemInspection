#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : SshHost.py
# @Author: xuxuedong
# @Date  : 2020/11/30
# @Desc

import paramiko
import re
from paramiko.rsakey import RSAKey
from io import StringIO
from lib.untils import exec_try_except
from paramiko.client import SSHClient, AutoAddPolicy

ignore_reg = re.compile(
    r"Error: JAVA_HOME is not set and could not be found"
    r"|stty: standard input: Inappropriate ioctl for device"
)

class SSH (object):
    def __init__(self,hostname, port, username, password,pkey=None,connect_timeout=10):
        self.client = None
        self.arguments = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'pkey': RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            'timeout': connect_timeout,
        }
    @exec_try_except
    def exec_command(self, command, timeout=1800, environment=None):

        if self.arguments["username"] != 'root':
            command = "sudo " + command
        command = 'set -e\n' + command
        # print(type(self))
        #with 这个实例实例是会执行__enter__函数从而获取到client连接
        with self as cli:
            # print(cli)
            chan = cli.get_transport().open_session()
            chan.settimeout(timeout)
            chan.set_combine_stderr(True)
            if environment:
                str_env = ' '.join(f"{k}='{v}'" for k, v in environment.items())
                print(str_env)
                command = f'export {str_env} && {command}'
            command = f"source /etc/profile; {command}"
            print(command)
            chan.exec_command(command)
            #创建buffer
            out = chan.makefile("r", -1).read()
            if isinstance(out, bytes):
                out = out.decode("utf-8")
            # output filter some line match the ignore_regs
                out = "\n".join([line for line in out.split("\n") if not ignore_reg.search(line)])
            return chan.recv_exit_status(), out
    def get_client(self):
        #进行ssh连接
        if self.client is not None:
            return self.client
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy)
        self.client.connect(**self.arguments)
        return self.client
    def __enter__(self):
        self.client = None
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client = None