#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : log.py
# @Author: xuxuedong
# @Date  : 2020/11/28
# @Desc

import sys
import logging
from logging import handlers

colors = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'red': '\033[91m',
          'ENDC': '\033[0m', 'bold': '\033[1m', 'underline': '\033[4m'}


def str_color(color, data):
    # return colors[color] + str(data) + colors['ENDC']
    return colors[color] + str(data) + colors['ENDC']


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, filename=None, level='debug', when='D', back_count=3, msg_fmt='%(message)s'):
        self.logger = logging.getLogger("healcheck")
        self.filelogger = logging.getLogger(filename)

        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

        if not self.filelogger.handlers:
            self.filelogger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        # self._sh_fmt = '[%(asctime)s] - %(filename)s[line:%(lineno)4d] - %(levelname)7s: %(message)s'
        self._sh_fmt = msg_fmt
        self._sh_format_str = logging.Formatter(self._sh_fmt)
        sh.setFormatter(self._sh_format_str)
        sh.setLevel(self.level_relations.get(level))
        self.logger.addHandler(sh)

        # file
        if filename is not None:
            fh = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count,
                                                   encoding='utf-8')
            # self._fh_fmt = '[%(asctime)s] - %(filename)s[line:%(lineno)4d] - %(levelname)7s: %(message)s'
            self._fh_fmt = msg_fmt
            self._fh_format_str = logging.Formatter(self._fh_fmt)
            fh.setFormatter(self._fh_format_str)
            fh.setLevel(logging.DEBUG)
            self.logger.addHandler(fh)
            self.filelogger.addHandler(fh)

    def set_level(self, level):
        self.logger.setLevel(self.level_relations.get(level, "info"))

    def debug(self, msg, color="underline"):
        self.logger.debug(str_color(color, msg))

    def info(self, msg, color="green"):
        self.logger.info(str_color(color, msg))

    def warn(self, msg, color="yellow"):
        self.logger.warning(str_color(color, msg))

    def error(self, msg, color="red"):
        self.logger.error(str_color(color, msg))

    def critical(self, msg, color="red"):
        self.logger.critical(str_color(color, msg))
