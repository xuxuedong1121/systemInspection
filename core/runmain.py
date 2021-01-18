#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: xuxuedong
# @Date  : 2020/11/27
# @Desc

import argparse,os,json
from core.log import str_color,Logger
from core.taskdata import TasksData
from core.corehandler import HealthCheck as hlt
from core.operations import LoginHost
from lib.untils import CustomEncoder
from core.createconf import CreateConf

import time
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
def runtask(hlt,task,log_level='info'):
    '''
    运行任务
    :param task:本次巡查的产品;hlt:将健康检查核心类传入方便函数内部调用。
    所需动作lambda 表达式创建日志目录
    :return:
    '''
    print("CURRENT_PATH:"+CURRENT_PATH)
    start_time = int(time.time())
    tim = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    logdir = os.path.join(CURRENT_PATH, os.pardir, "logs")
    logfile = os.path.join(CURRENT_PATH, os.pardir, f"logs/{task}-healcheck{tim}.log")
    mkdirlambda = lambda x: os.makedirs(logdir) if not os.path.exists(logdir) else True
    mkdirlambda(logdir)
    log = Logger(logfile,log_level)
    hlt.logger = log.logger
    hlt.filloger = log.filelogger
    #获取运行任务中yaml文件数据
    tasksdata = TasksData(task).get_taskdata()
    hlt.logger.info("%s" % tasksdata["name"])
    '''
    获取plugins中所有的插件类得到dic
    '''
    plugins = hlt.get_plugins()
    # 统计检查项
    ret_json = {}
    total_count = 0
    succ_count = 0
    fail_count = 0
    warn_count = 0
    for task in tasksdata['tasks']:
        ret_json[task["name"]] = {}
        hlt.logger.info(f"|-- {task['name']}")
        # print(task)
        if 'hosts' in task and not isinstance(task['hosts'],list):
            raise Exception(f"task {task['hosts']} must be list type")
        if 'hosts' not in task and len(task['hosts']==0):
            task['hosts']=['127.0.0.1']
        # print(task['name'],list(set(task["hosts"])))
        for host in list(set(task["hosts"])):
            hs = host.split(",")[0]
            ret_json[task["name"]][hs] = {}
            hlt.logger.info(f'|   |-- {hs}主机巡检')
            #获取runner实例
            runner = LoginHost(host)
            for r in task['roles']:
                # 获取插件dic中的的类
                plugin = plugins.get(r['role'])
                # print("plugin",plugin)
                if not plugin:
                    raise Exception(f"plugin:{r['role']} not found")
                # print(r.get('funcs'))
                # _kwargs = {}
                # if r.get('kwargs') is not  None:
                #     for key in r['kwargs']:
                #         print(key)
                #         _kwargs[key] = r['kwargs'][key]
                #         print(_kwargs)
                '''
                plugin中继承了HealthCheck，在HealthCheck中__init__(self,runner)需要传入runner并返回有self.runner
                传入后实例化实例化p_instance这个类后,调用p_instance()是调用__call__方法传入funcs解析当中的方法；
                传入funcs:[{'func': 'mem_useage'}, {'func': 'load_average', 'desc': '检查最近5分钟系统平均负载是否小于CPU核数', 'args': {'N': 5}}, {'func': 'sync_date'}, {'func': 'ping'}, {'func': 'ping_delay',
 'desc': 'ping网络延迟小于 1 ms', 'args': {'max_ms': 1}}, {'func': 'partition_useage', 'desc': '检查挂载点 / 使用率小于80%', 'args': {'mountpoint': '/'}}, {'func': 'partition_useage',
'desc': '检查挂载点 /data 使用率小于80%', 'args': {'mountpoint': '/data'}}]
                '''
                p_instance = plugin(runner=runner)
                # print(p_instance(r.get('funcs')))
                rets = p_instance(r.get("funcs"))
                hlt.logger.debug(rets)
                # print(rets)
                ret_json[task["name"]][hs][r["role"]] = rets
                # print("ret_json",ret_json)
                ret_codes = [r['status'] for r in rets]
                total_count += len(ret_codes)
                succ_count += ret_codes.count(hlt.SUCCESS_STATUS_CODE)
                fail_count += ret_codes.count(hlt.FAILED_STATUS_CODE)
                warn_count += ret_codes.count(hlt.WARN_STATUS_CODE)

    hlt.logger.info(u"--- 统计 ---\nTotal: %s Success: %s Failed: %s Warning: %s Time: %ds\n" % (
                total_count, str_color("green", succ_count), str_color("red", fail_count),
                str_color("yellow", warn_count),
                int(time.time()) - start_time))

    return ret_json



def get_alltask():
    '''
    获取在\shell\systemInspection\task目录下所有的子目录，子目录里面为所有的需要检测的服务配置yaml
    :return:返回一个list，list中包含task目录中的子目录如：[ cvm, mysql, vpc]
    '''
    TASK_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),os.pardir,'task')
    return [x for x in os.listdir(TASK_PATH) if os.path.isdir(os.path.join(TASK_PATH, x))]
def main():
    parser = argparse.ArgumentParser(description='健康检查结果')
    parser.add_argument('-p', '--product', type=str, dest='product',
                        help=u'指定巡检产品：如 cvm, mysql, vpc, 传入 all 则巡检 tasks 下所有产品')
    parser.add_argument('-b', '--build', type=str, dest='bulid', help='Build configuration file')
    parser.add_argument('-d', '--debug', type=str, dest='debug', help=u'开启程序运行dubug功能')


    args = parser.parse_args()
    print('argss;',args)
    product = args.product
    bulid = args.bulid
    if not product and not bulid:
        parser.print_help()
        return
    check_products = get_alltask()
    prods_data = {}
    need_check_products = []
    if bulid is not None :
        if bulid.lower() == 'all':
            need_check_products = check_products
            for pl in need_check_products:
                CreateConf(pl)
        else:
            pro_list = [pro.strip() for pro in bulid.split(",")]
            for pl in pro_list:
                if pl.lower() in check_products:
                    need_check_products.append(pl.lower())
                # else:
                #     print(str_color("red", f"输入的 {pl} 不在巡检产品列表，请输入正确的产品名称，如：{check_products}"))
    if product is not None:
        if product.lower() == 'all':
           need_check_products = check_products
        else:
            '''
            如果-p mysql,rio那么 product= mysql,rio 
            用‘，’分割构造成新的列表['rio', 'mysql']
            '''
            pro_list = [pro.strip() for pro in product.split(",")]
            '''
            从pro_list列表中将，将列表中子母进行小写转换（在task中的所有目录为小写）并判断所输入的-p 参数
            在check_products中是否存在如果存在加入need_check_products列表中；
            如果不存在打印错误
            '''
            for pl in pro_list:
                if pl.lower() in check_products:
                    need_check_products.append(pl.lower())
                else:
                    print(str_color("red",f"输入的 {pl} 不在巡检产品列表，请输入正确的产品名称，如：{check_products}"))
        if len(need_check_products) > 1:
            filename = "all"
        else:
            filename = need_check_products[0]
        for pol in need_check_products :
            '''
            pol为本次巡查的产品need_check_products为需要巡查的产品列表,运行任务返回数据为字典形式        
            '''
            try:
                check_data_dir = runtask(hlt,pol)
            except Exception as e :
                print(e)
            prods_data[pol] = check_data_dir
            # 产品巡检 json 数据待处理, 传入API或写入本地文件
            json_dir = os.path.join(CURRENT_PATH, os.pardir, "jdata", filename)
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)

            json_file = f"{filename}-{time.strftime('%Y%m%d%H%M%S', time.localtime())}.json"
            with open(os.path.join(json_dir, json_file), "w", encoding='utf-8') as f:
                f.write(json.dumps(prods_data, cls=CustomEncoder, ensure_ascii=False, indent=4))