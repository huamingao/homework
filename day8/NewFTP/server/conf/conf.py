#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys

# 工作目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_ADDR = ('localhost', 6969)
INVENTORY_DIR = os.path.join(PROJECT_DIR, 'db', 'inventory')
USER_OBJ_DIR = os.path.join(PROJECT_DIR, 'db', 'user_obj')
USER_HOME_DIR = os.path.join(PROJECT_DIR, 'db', 'user_home')


# server_socket()
START_LISTEN = '服务端开始监听了！'
COMPLETE_REQUEST = '客户端请求处理完毕！'
CLOSE_COON = '本次连接已关闭!'

# handle_request()
CHECK_NAME = '检查用户名'
REGISTER = '注册用户'
LOGIN = '登录用户'
RUN_CMD = '我要执行系统命令'
LOGOFF = '注销登录'
LIST_INVENTORY = '以下是公共目录中的文件列表:\n'
OVERWRITE_FILE_INVENTORY = '覆盖公共目录中的文件'
OVERWRITE_FILE_HOME = '覆盖家目录中的文件'
INVALID_INPUT = '您的输入有误，请重新输入!'

# check_name()
NAME_EXIST = '该用户名已被占用！请尝试输入其他用户名！'
NAME_NO_EXIST = '您输入的用户名不存在！注册？y/n:'

# register()
SUCCESS_REGISTER = '恭喜您已成功注册！下面自动跳转到登录界面...'

#login()
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = ', 您已成功登录FTP系统！'

# run_cmd()
CREATE_HOME_DIR = '用户家目录尚不存在，自动创建用户家目录'
SEND_CLIENT_RES = '服务端执行了系统命令，正在向客户端发送执行结果...'
SUCCESS_RUN_CMD = '没有消息就是好消息！如果你是在查看目录，说明现在目录为空'

# print_home_dir()
PRINT_HOME_DIR = '打印用户家目录'

# print_inventory_dir()
PRINT_INVENTORY_DIR = '打印公共目录'

# upload()
SUCCESS_UPLOAD = '文件已成功上传到公共目录'
NO_UPLOAD_FILE = '您要上传的文件不存在！'
FILE_EXIST_INVENTORY = '公共目录中已存在同名文件，是否覆盖？y/n:'

# download()
NO_DOWNLOAD_FILE = '您要下载的文件不存在！'
SUCCESS_DOWNLOAD = '文件已成功下载到家目录'
FILE_EXIST_HOME = '家目录中已存在同名文件，是否覆盖？y/n:'
