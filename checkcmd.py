#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cmd.py
# @Author: xuxuedong
# @Date  : 2020/11/26
# @Desc


import os, sys,argparse
from jinja2 import PackageLoader, Environment
import yaml
from core.runmain import main



CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

CORE_PATH = os.path.join(CURRENT_PATH, 'core')

if CORE_PATH not in sys.path:
    sys.path.append(CORE_PATH)

PKG_PATH = os.path.join(CURRENT_PATH, 'pkg')
if PKG_PATH not in sys.path:
    sys.path.append(PKG_PATH)



if __name__ == '__main__':
    version = 'v1.2'
    program = u'''
               _                 _                           _   _             
 ___ _   _ ___| |_ ___ _ __ ___ (_)_ __  ___ _ __   ___  ___| |_(_) ___  _ __  
/ __| | | / __| __/ _ \ '_ ` _ \| | '_ \/ __| '_ \ / _ \/ __| __| |/ _ \| '_ \ 
\__ \ |_| \__ \ ||  __/ | | | | | | | | \__ \ |_) |  __/ (__| |_| | (_) | | | |
|___/\__, |___/\__\___|_| |_| |_|_|_| |_|___/ .__/ \___|\___|\__|_|\___/|_| |_|
     |___/                                  |_|                                 %s
        ''' % version
    print(program)
    main()