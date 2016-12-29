#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
import json
from src import crontab as src_crontab



# 要求用户输入一串数字，输错打印'输入不合法'，直至输入合法为止
def force_digit(msg_prompt,invalid_msg):
    while True:
        input_msg = input(msg_prompt)
        if input_msg == 'q':
            return 'q'
        if not input_msg.isdigit():
            print(invalid_msg)
        else:
            break
    return int(input_msg)





