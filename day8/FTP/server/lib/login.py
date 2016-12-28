#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import getpass
import pickle
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGFILE = os.path.join(PROJECT_DIR,'db','server','log')

from bin import main
from src import user
from lib import logger

# User类的交互文字
FAIL_LOGIN = '登录失败，请重新尝试登录'
INPUT_NAME = '请输入登录用户名(直接输回车将退回到欢迎界面)：'
REGISTER_NAME = '请输入要注册的用户名(直接输回车将退回到欢迎界面)：'
INVALID_NAME = '您输入的用户名不存在！注册？y/n:'
INPUT_PWD = '请输入登录密码：'
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = ', 您已成功登录FTP系统！'
NAME_EXIST = '该用户名已被占用！请尝试输入其他用户名！'
SET_PWD = '正在为您注册用户名{0}，请设置登录密码:'
SUCCESS_REGISTER = '恭喜您已成功注册！下面自动跳转到初始界面...'
MSG_REGISTER = 'User {0} Registered'
MSG_LOGIN = 'User {0} Logined'

def register():
    """
    新用户注册
    :param :
    :return:
    """
    while True:
        name = input(REGISTER_NAME)
        if name == '':
            main.main()
        else:
            # 查看用户文件在服务端是否存在
            user_file = os.path.join(PROJECT_DIR,'db','server','users',name)
            # 如果账户存在，提示账户名已被占用
            if os.path.exists(user_file):
                print(NAME_EXIST)
                continue
            # 如果账户不存在，注册产生账户文件
            else:
                try:
                    # getpass is only for linux platform
                    password = getpass.getpass(SET_PWD.format(name))
                    #password = input(SET_PWD.format(name))
                    # 在客户端上创建用户家目录
                    hmdir = os.path.join(PROJECT_DIR,'db','client','home',name)
                    os.mkdir(hmdir)
                    # 创建用户对象
                    user_obj = user.User(name,password,hmdir)
                    # 在服务端上生成用户对象文件
                    with open(os.path.join(user_file), 'wb') as f:
                        pickle.dump(user_obj,f)
                    print(SUCCESS_REGISTER)
                    # 在服务端创建日志文件，并写入一条日志
                    logger.logger(LOGFILE, MSG_REGISTER.format(name))
                    main.main()
                except:
                    if os.path.exists(user_file):del user_file
                    if os.path.exists(hmdir):del hmdir


def login():
    """
    用户登录
    :return:
    """
    while True:
        name = input(INPUT_NAME)
        if name == '':
            main.main()
        else:
            user_file = os.path.join(PROJECT_DIR,'db','server','users',name)
            # 如果账账户文件存在，获取账号对象
            if os.path.exists(user_file):
                user_obj = pickle.load(open(user_file, 'rb'))
                # for windows platform
                #input_pwd = input(INPUT_PWD)
                # for linux platform
                input_pwd = getpass.getpass(INPUT_PWD)
                # 从文件读取user对象
                if input_pwd != user_obj.password:
                    print(INVALID_PWD)
                    continue
                else:
                    print(user_obj.name,SUCCESS_LOGIN)
                    logger.logger(LOGFILE, MSG_LOGIN.format(name))
                    user_obj.show_options()
            # 如果账号文件不存在，询问是否调转到注册界面
            else:
                option = input(INVALID_NAME)
                # 输入y则跳转到新用户注册，否则跳转到欢迎界面
                if option == 'y':
                    register()
                    continue
                else:
                    main.main()



