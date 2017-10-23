#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import socket
from bin import main
from conf.conf import *
import subprocess

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
                # getpass is only for linux platform
                # password = getpass.getpass(SET_PWD.format(name))
                # for windows platform
                password = input(SET_PWD.format(name))
                res = User.socket_client(REGISTER, name, password)
                if res == NAME_EXIST.encode('utf-8'):
                    print(NAME_EXIST)
                    continue
                elif res == SUCCESS_REGISTER.encode('utf-8'):
                    os.mkdir(os.path.join(USER_HOME_DIR,name))
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
                # 根据服务端返回的数据，在客户端显示登录结果
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
        user_obj.main()

    def upload(self,filename):
        # 判断家目录中是否存在该文件
        hmdir_file = os.path.join(USER_HOME_DIR,self.name,filename)
        if not os.path.exists(hmdir_file):
            print(NO_UPLOAD_FILE)
        # 如果要上传的文件在公共目录已存在，提示是否覆盖
        else:
            with open(hmdir_file, 'rb') as f:
                content = f.read().decode('utf-8')
            res = User.socket_client(UPLOAD,filename,content)
            if res != FILE_EXIST_INVENTORY.encode('utf-8'):
                print(res.decode('utf-8'))
            else:
                option = input(FILE_EXIST_INVENTORY)
                if option != 'y':
                    print(CANCELL_UPLOAD)
                else:
                    print(SUCCESS_UPLOAD)

    def confirm_download(self,filename):
        res = User.socket_client(DOWNLOAD, filename)
        # 如果返回<您要下载的文件不存在！>
        if res == NO_DOWNLOAD_FILE.encode('utf-8'):
            print(NO_DOWNLOAD_FILE)
        # 否则返回的是文件内容
        else:
            with open(os.path.join(USER_HOME_DIR, self.name,filename), 'wb') as f:
                f.write(res)
            print(SUCCESS_DOWNLOAD)

    def download(self,filename):
        # 判断家目录是否存在同名文件
        hmdir_file = os.path.join(USER_HOME_DIR, self.name,filename)
        if not os.path.exists(hmdir_file):
            self.confirm_download(filename)
        else:
            # 询问是否覆盖现有文件
            if input(FILE_EXIST_HOME) != 'y':
                print(CANCELL_DOWNLOAD)
            # 输入y,表示同意覆盖，继续下载文件
            else:
                self.confirm_download(filename)

    def list_home(self):
        """
        列出家目录文件列表
        :return:
        """
        # for Windows
        obj = subprocess.Popen("dir", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=os.path.join(USER_HOME_DIR,self.name))
        # # for Linux
        # obj = subprocess.Popen("ls -l", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                     cwd=os.path.join(USER_HOME_DIR,self.name))
        stdout,stderr = obj.communicate()
        print(LIST_HOME,stdout.decode('utf-8'),stderr.decode('utf-8'))

    @staticmethod
    def list_inventory():
        """
        列出公共目录文件列表
        :return:
        """
        res = User.socket_client(LIST)
        print(LIST_INVENTORY,res.decode('utf-8'))

    def run_cmd_on_server(self,cmd):
        res = User.socket_client(RUN_CMD,cmd)
        print(res.decode('utf-8'))

    def main(self):
        """
        登录后提示用户输入命令
        :return:
        """
        while True:
            cmd = input(WAIT_INPUT_CMD)
            try:
                # 如果输入exit,就跳出循环，返回到欢迎界面
                if cmd == 'exit':
                    print(MSG_LOGOFF.format(self.name))
                    break
                # 上传
                elif cmd.startswith('upload'):
                    self.upload(cmd.replace('upload ',''))
                # 下载
                elif cmd.startswith('download'):
                    self.download(cmd.replace('download ',''))
                # 列出公共目录文件列表
                # for windows
                elif cmd == 'dir':
                # # for linux
                #elif cmd == 'ls':
                    User.list_inventory()
                # 列出家目录文件列表
                # for windows
                elif cmd == 'dir home':
                # # for linux
                # elif cmd == 'ls home':
                    self.list_home()
                # 执行系统命令
                else:
                    self.run_cmd_on_server(cmd)
            # 捕获所有异常，提示输入不合法
            except:
                print(INVALID_INPUT)
        main.main()


