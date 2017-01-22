#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import socket
from bin import main
from conf.conf import *


class User(object):

    def __init__(self,name,password):
        self.name = name
        self.password = password

    @staticmethod
    def socket_client(*data):
        """
        客户端向服务端发起请求
        :param data: 要发给服务端的数据
        :return: 服务端发回的数据
        """
        data = '+'.join(data)
        # 在客户端创建一个socket对象
        client = socket.socket()
        client.connect(SERVER_ADDR)
        client.send(data.encode('utf-8'))
        # 此处服务端正在另一头处理请求...获取服务端返回的数据
        res = client.recv(102400000)
        # 结束连接
        client.close()
        # 返回数据
        return res

    @staticmethod
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
                res = User.socket_client(CHECK_NAME,name)
                if res == NAME_EXIST.encode('utf-8'):
                    print(NAME_EXIST)
                    continue
                elif res == NAME_NO_EXIST.encode('utf-8'):
                    # getpass is only for linux platform
                    # password = getpass.getpass(SET_PWD.format(name))
                    # for windows platform
                    password = input(SET_PWD.format(name))
                    res = User.socket_client(REGISTER, name, password)
                    if res == SUCCESS_REGISTER.encode('utf-8'):
                        print(SUCCESS_REGISTER)
                        User.login()

    @staticmethod
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
                # for windows platform
                password = input(INPUT_PWD)
                # for linux platform
                # input_pwd = getpass.getpass(INPUT_PWD)
                res = User.socket_client(LOGIN,name,password)
                if res == NAME_NO_EXIST.encode('utf-8'):
                    option = input(NAME_NO_EXIST)
                    if option == 'y':
                        User.register()
                    else:
                        continue
                elif res == INVALID_PWD.encode('utf-8'):
                    print(INVALID_PWD)
                    continue
                elif res == SUCCESS_LOGIN.encode('utf-8'):
                    print(name,SUCCESS_LOGIN)
                    break
        user_obj = User(name, password)
        User.print_inventory_dir()
        user_obj.print_home_dir()
        user_obj.run_cmd()

    def run_cmd(self):
        """
        打印用户菜单选项
        :return:
        """
        while True:
            cmd = input(WAIT_INPUT_CMD)
            try:
                # 如果输入exit,就跳出循环，返回到欢迎界面
                if cmd == 'exit':
                    print(MSG_LOGOFF.format(self.name))
                    break
                else:
                    res = User.socket_client(RUN_CMD,self.name,cmd)
                    # 如果要上传的文件在公共目录已存在，提示是否覆盖
                    if res == FILE_EXIST_INVENTORY.encode('utf-8'):
                        if input(res.decode('utf-8')) == 'y':
                            res = User.socket_client(OVERWRITE_FILE_INVENTORY,self.name,cmd)
                        else:
                            res = CANCELL_UPLOAD
                    # 如果要下载的文件在家目录已存在，提示是否覆盖
                    if res == FILE_EXIST_HOME.encode('utf-8'):
                        if input(res.decode('utf-8')) == 'y':
                            res = User.socket_client(OVERWRITE_FILE_HOME,self.name,cmd)
                        else:
                            res = CANCELL_DOWNLOAD.encode('utf-8')
                    print(SHOW_RESULT,res.decode('utf-8'))
                    # 如果成功执行了上传文件的命令，打印公共目录文件列表
                    if res == SUCCESS_UPLOAD.encode('utf-8'):
                        res = User.socket_client(LIST_INVENTORY)
                        print(LIST_INVENTORY,res.decode('utf-8'))
            # 捕获所有异常，提示输入不合法
            except:
                print(INVALID_INPUT)
        main.main()

    def print_home_dir(self):
        res = User.socket_client(PRINT_HOME_DIR, self.name)
        print('当前位置为您的家目录：{0}'.format(res.decode('utf-8')))
    
    @staticmethod
    def print_inventory_dir():
        res = User.socket_client(PRINT_INVENTORY_DIR)
        print('公共目录位于：{0}'.format(res.decode('utf-8')))
