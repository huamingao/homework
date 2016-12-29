#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import pickle
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)
USERS_DIR = os.path.join(PROJECT_DIR,'db','users')

from src import user as src_user


INPUT_OPTION = '''
欢迎登录选课系统！
1. 登录
2. 注册
继续请输编号，退出请输任意其他键：'''

if __name__ == "__main__":

    # 程序自动生成一个默认管理员账号，账户admin，密码pwd
    admin_file = os.path.join(PROJECT_DIR, 'db', 'admin')
    admin_obj = src_user.Admin('admin', 'pwd')
    pickle.dump(admin_obj, open(admin_file, 'wb'))

    option = input(INPUT_OPTION)

    if option == '1':
        src_user.User.login()
    elif option == '2':
        src_user.User.register_user()
    else:
        exit()






