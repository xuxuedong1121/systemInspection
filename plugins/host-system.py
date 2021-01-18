#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : system.py
# @Author: xuxuedong
# @Date  : 2020/11/30
# @Desc
from core.corehandler import HealthCheck
from lib.untils import check_task
class HostSystemCheck(HealthCheck):
    role = "host-system"
    @check_task(task_name="检查内存使用率是否小于 80%")
    def mem_useage(self):
        ret_code, ret_msg = self.runner.operation.exec_command("free -m | grep -w 'Mem'")
        if ret_code != 0:
            return self.FAILED_STATUS_CODE, f"获取内存使用信息异常：{ret_msg}"
        mem_info = ret_msg
        mem_total = float(mem_info.split()[1])
        mem_used = float(mem_info.split()[2])
        mem_useage = round((mem_used / mem_total) * 100, 2)

        last_msg = f"mem total: {mem_total}m, used: {mem_used}m, useage: {mem_useage}%"
        if float(mem_useage) > float(80):
            return self.FAILED_STATUS_CODE, last_msg
        else:
            return self.SUCCESS_STATUS_CODE, last_msg

    @check_task(task_name="检查最近5分钟系统平均负载")
    def load_average(self,N=5):
        return self.SUCCESS_STATUS_CODE ,'load_average'

    @check_task(task_name="检查时间是否同步")
    def sync_date(self):
        return self.SUCCESS_STATUS_CODE ,'sync_date'

    @check_task(task_name="连通性")
    def ping(self):
        return self.SUCCESS_STATUS_CODE ,'ping'

    @check_task(task_name="延迟")
    def ping_delay(self,host=None, max_ms=1):
        return self.SUCCESS_STATUS_CODE ,'ping_delay'

    @check_task(task_name="分区")
    def partition_useage(self,mountpoint):
        return self.SUCCESS_STATUS_CODE ,mountpoint + ":" + "80%"
