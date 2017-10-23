#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os

# 工作目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_ADDR = ('localhost', 6969)
INVENTORY_DIR = os.path.join(PROJECT_DIR, 'db', 'inventory')
USER_OBJ_DIR = os.path.join(PROJECT_DIR, 'db', 'user_obj')

# server_socket()
START_LISTEN = '服务端开始监听了！'
COMPLETE_REQUEST = '客户端请求处理完毕！'
CLOSE_COON = '本次连接已关闭!'

# handle_request()
REGISTER = '注册'
LOGIN = '登录'
UPLOAD = '上传'
DOWNLOAD = '下载'
LIST = '列出公共目录'
RUN_CMD = '执行系统命令'
INVALID_INPUT = '您的输入有误，请重新输入!'

# register()
SUCCESS_REGISTER = '恭喜您已成功注册！下面自动跳转到登录界面...'
NAME_EXIST = '该用户名已被占用！请尝试输入其他用户名！'

#login()
NAME_NO_EXIST = '您输入的用户名不存在！注册？y/n:'
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = ', 您已成功登录FTP系统！'

# run_cmd()
CREATE_HOME_DIR = '用户家目录尚不存在，自动创建用户家目录'
SEND_CLIENT_RES = '服务端执行了系统命令，正在向客户端发送执行结果...'
SUCCESS_RUN_CMD = '没有消息就是好消息！如果你是在查看目录，说明现在目录为空'

# upload()
SUCCESS_UPLOAD = '文件已成功上传到公共目录'
NO_UPLOAD_FILE = '您要上传的文件不存在！'
FILE_EXIST_INVENTORY = '公共目录中已存在同名文件，是否覆盖？y/n:'

# download()
NO_DOWNLOAD_FILE = '您要下载的文件不存在！'
SUCCESS_DOWNLOAD = '文件已成功下载到家目录'
FILE_EXIST_HOME = '家目录中已存在同名文件，是否覆盖？y/n:'
