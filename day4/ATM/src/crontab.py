#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import sys
import os
import json
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DB = os.path.join(PROJECT_DIR,'db')
sys.path.append(PROJECT_DIR)

from src import crontab as src_crontab
from src import admin as src_admin
from src import client as src_client




# main函数用到的交互文字
MENU = """
欢迎来到信用卡管理平台！
1、普通用户入口
2、管理员入口
退出整个程序，请输q
"""
OPTION_PROMPT = '请输入您的选项：'
EXIT_MSG = '您已成功退出信用卡管理平台'
INVALID_MSG = '您的输入不合法，请重新输入！'



def main():
    print(MENU)
    while True:
        menu_option = input(OPTION_PROMPT)
        if menu_option == 'q':
            # 输q退出程序
            print(EXIT_MSG)
            exit()
        elif menu_option == '1':
            # 普通用户入口
            src_client.main()
        elif menu_option == '2':
            # 管理员入口
            src_admin.main()
        else:
            # 输入不合法
            print(INVALID_MSG)