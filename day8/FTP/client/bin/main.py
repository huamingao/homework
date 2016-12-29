#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)


from lib import login



WEL_INFO = '''
欢迎来到简单FTP程序！
1. 登录
2. 注册
3. 退出
请输入编号:'''
INVALID_OPTION = '您输入的选项不存在，请重新输入!'


def main():
    while True:
        option = input(WEL_INFO)
        if option == '3':
            exit()
        elif option == '1':
            login.login()
        elif option == '2':
            login.register()
        else:
            print(INVALID_OPTION)

if __name__ == '__main__':
    main()
