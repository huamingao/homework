#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


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
CHECK_NAME = '检查用户名'
REGISTER = '注册用户'

#user.login()
INPUT_NAME = '请输入登录用户名(直接输回车将退回到欢迎界面)：'
INPUT_PWD = '请输入登录密码：'
FAIL_LOGIN = '登录失败，请重新尝试登录'
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = ', 您已成功登录FTP系统！'
LOGIN = '登录用户'
LOGOFF = '注销登录'

# user.run_cmd()
WAIT_INPUT_CMD = '''
（支持系统命令如pwd,ls,touch等，支持自定义命令upload <filename>, download <filename>，注销请输exit）
请输入要执行的命令：'''
INVALID_INPUT = '您的输入有误，请重新输入!'
MSG_LOGOFF = '{0}, 您已成功注销登录'
RUN_CMD = '我要执行系统命令'
SHOW_RESULT = '以下是执行结果:\n'
LIST_INVENTORY = '以下是公共目录中的文件列表:\n'

# user.print_home_dir()
PRINT_HOME_DIR = '打印用户家目录'

# user.print_inventory_dir()
PRINT_INVENTORY_DIR = '打印公共目录'

# user.upload()
SUCCESS_UPLOAD = '文件已成功上传到公共目录'
NO_UPLOAD_FILE = '您要上传的文件不存在！'
FILE_EXIST_INVENTORY = '公共目录中已存在同名文件，是否覆盖？y/n:'
OVERWRITE_FILE_INVENTORY = '覆盖公共目录中的文件'
CANCELL_UPLOAD = '取消文件上传'

# user.download()
NO_DOWNLOAD_FILE = '您要下载的文件不存在！'
SUCCESS_DOWNLOAD = '文件已成功下载到家目录'
FILE_EXIST_HOME = '家目录中已存在同名文件，是否覆盖？y/n:'
OVERWRITE_FILE_HOME = '覆盖家目录中的文件' 
CANCELL_DOWNLOAD = '取消文件下载'
