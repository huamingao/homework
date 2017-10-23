#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_HOME_DIR = os.path.join(PROJECT_DIR, 'db', 'user_home')

# 服务端通信端口
SERVER_ADDR = ('localhost', 6969)

# main.main()
WEL_INFO = '''
欢迎来到简单FTP程序！
1. 登录
2. 注册
3. 退出
请输入编号:'''
INVALID_INPUT = '您的输入有误，请重新输入!'

# user.register()
REGISTER_NAME = '请输入要注册的用户名(直接输回车将退回到欢迎界面)：'
SET_PWD = '正在为您注册用户名{0}，请设置登录密码:'
NAME_EXIST = '该用户名已被占用！请尝试输入其他用户名！'
NAME_NO_EXIST = '您输入的用户名不存在！注册？y/n:'
SUCCESS_REGISTER = '恭喜您已成功注册！下面自动跳转到登录界面...'
REGISTER = '注册'

#user.login()
INPUT_NAME = '请输入登录用户名(直接输回车将退回到欢迎界面)：'
INPUT_PWD = '请输入登录密码：'
FAIL_LOGIN = '登录失败，请重新尝试登录'
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = ', 您已成功登录FTP系统！'
LOGIN = '登录'

# user.main()
WAIT_INPUT_CMD = '''
（支持自定义命令upload 文件名, download 文件名,dir, dir home，注销请输exit）
请输入要执行的命令：'''
INVALID_INPUT = '您的输入有误，请重新输入!'
MSG_LOGOFF = '{0}, 您已成功注销登录'
RUN_CMD = '执行系统命令'
SHOW_RESULT = '以下是执行结果:\n'


# user.upload()
UPLOAD = '上传'
SUCCESS_UPLOAD = '文件已成功上传到公共目录'
NO_UPLOAD_FILE = '您要上传的文件不存在！'
FILE_EXIST_INVENTORY = '公共目录中已存在同名文件，是否覆盖？y/n:'
OVERWRITE_FILE_INVENTORY = '覆盖公共目录中的文件'
CANCELL_UPLOAD = '取消文件上传'

# user.download()
DOWNLOAD = '下载'
NO_DOWNLOAD_FILE = '您要下载的文件不存在！'
SUCCESS_DOWNLOAD = '文件已成功下载到家目录'
FILE_EXIST_HOME = '家目录中已存在同名文件，是否覆盖？y/n:'
OVERWRITE_FILE_HOME = '覆盖家目录中的文件' 
CANCELL_DOWNLOAD = '取消文件下载'

#user.list_inventory()
LIST = '列出公共目录'
LIST_INVENTORY = '以下是公共目录中的文件列表:\n'

#user.list_home()
LIST_HOME = '以下是家目录中的文件列表:\n'
