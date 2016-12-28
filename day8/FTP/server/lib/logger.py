#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import logging

def logger(log_file,message):
    """
    操作记录
    :param message:
    :return:
    """
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(message)