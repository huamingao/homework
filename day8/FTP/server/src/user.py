#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import socket
from bin import main

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_DIR = os.path.join(PROJECT_DIR, 'db','server', 'inventory')
SERVER_ADDR = ('localhost', 6969)
LOGFILE = os.path.join(PROJECT_DIR,'db','server','log')

OPTION_LIST = '''
您可以进行如下操作：
1.查看公共目录
2.查看家目录
3.上传：从家目录上传到公共目录
4.下载：从公共目录下载到家目录
5.查看操作记录
6.退出
请输入编号：'''
INVALID_OPTION = '您输入的选项不存在，请重新输入！'

ESTABLISH_CONN = '客户端正在向服务端请求建立连接...'
SEND_TO_SERVER = '客户端正在向服务端发送请求（{0}）...'
REC_FROM_SERVER = '客户端正在接收服务端返回的数据（{0}）...'

INVENTORY_CONTENT = '以下是服务端公共目录中的文件：'
HMDIR_CONTENT = '{0}, 以下是您家目录中的文件:\n'
INPUT_DOWNLOAD_FILE = '请输入你要下载的文件名：'
SUCCESS_DOWNLOAD = '文件已成功下载到您的家目录中：{0}'
NO_FILE_EXIST = '文件不存在'
NO_FILE = '当前目录中没有任何文件！'
INPUT_UPLOAD_FILE = '请输入你要上传的文件名：'
CANCEL_UPLOAD = '您已取消上传文件！'
WAIT_FOR_INPUT = '选项执行结束，继续操作请输任意键...'
MSG_LOGOFF = 'User {0} Logoff'
FILE_EXIST = '服务端已存在同名文件，是否覆盖？y/n:'
READY_GET_UPLOAD = '服务端已准备好接收客户端的上传'
SUCCESS_LOGOFF = '您已成功注销登录'
FILE_EXIST_HMDIR = '您的家目录中已有同名文件，是否覆盖？y/n:'
CANCEL_DOWNLOAD = '您已取消下载！'
NO_UPLOAD_FILE = '您要上传的文件不存在！'
NO_DOWNLOAD_FILE = '您要下载的文件不存在！'
RUN_CMD = '我要执行系统命令'
DOWNLOAD = '我要下载'
PREPARE_UPLOAD = '预备上传'
UPLOAD = '我要上传'
LOGOFF = '注销登录'
WRITE_LOG = '写日志'


class User(object):

    def __init__(self,name,password,hmdir):
        self.name = name
        self.password = password
        self.hmdir = hmdir

    def show_options(self):
        """
        打印用户菜单选项
        :return:
        """
        while True:
            option = input(OPTION_LIST)
            if option == '6':
                self.logoff()
                main.main()
            elif option == '1':
                User.list_inventory()
                input(WAIT_FOR_INPUT)
            elif option == '2':
                self.list_hmdir()
                input(WAIT_FOR_INPUT)
            elif option == '3':
                self.upload()
                input(WAIT_FOR_INPUT)
            elif option == '4':
                self.download()
                input(WAIT_FOR_INPUT)
            elif option == '5':
                self.show_log()
                input(WAIT_FOR_INPUT)
            else:
                print(INVALID_OPTION)

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
        #print(ESTABLISH_CONN, end='')
        client.connect(SERVER_ADDR)
        #print(SEND_TO_SERVER, end='')
        client.send(data.encode('utf-8'))
        # 此处服务端正在另一头处理请求...
        #print(REC_FROM_SERVER)
        res = client.recv(1024)
        # 结束连接
        client.close()
        # 返回从服务端拿到的数据
        return res

    def logoff(self):
        data = (LOGOFF, MSG_LOGOFF.format(self.name))
        data = '+'.join(data)
        res = User.socket_client(data)
        print(res.decode())

    def write_log(self,operation,filename):
        data = (WRITE_LOG,'{0} successfully {1} the file {2}'.format(self.name,operation,filename))
        data = '+'.join(data)
        User.socket_client(data)

    @staticmethod
    def list_inventory():
        """
        列出服务端上公共目录中的文件
        :return:
        """
        INVENTORY_DIR = os.path.join(PROJECT_DIR, 'db','server', 'inventory')
        # 如果公共目录为空，打印当前目录没有文件
        if not os.listdir(INVENTORY_DIR):
            print(NO_FILE)
        else:
            # # for windows platform
            # cmd = 'dir {0}'.format(INVENTORY_DIR)
            # for linux platform
            cmd = 'ls -l {0}'.format(INVENTORY_DIR)
            # 客户端向服务端发送请求，并从服务端获得执行结果res
            res = User.socket_client(RUN_CMD,cmd)
            print(INVENTORY_CONTENT)
            # 打印返回的数据到客户端屏幕
            print(res.decode())

    @staticmethod
    def check_server(filename):
        """
        客户端向服务端发送文件前，检查服务端是否存在同名文件
        :param hmdir_file: 客户端家目录中该文件的绝对路径
        :return:
        """
        res = User.socket_client(PREPARE_UPLOAD, filename)
        if res == READY_GET_UPLOAD.encode('utf-8'):
            return True
        elif res == FILE_EXIST.encode('utf-8'):
            option = input(FILE_EXIST)
            if option == 'y':
                return True
            else:
                print(CANCEL_UPLOAD)
                return None

    @staticmethod
    def check_client(hmdir_file):
        """
        客户端接收服务端发来的文件前，检查客户端是否存在同名文件
        :param hmdir_file: 客户端家目录中该文件的绝对路径
        :return:
        """
        if not os.path.exists(hmdir_file):
            return True
        else:
            option = input(FILE_EXIST_HMDIR)
            if option == 'y':
                return True
            else:
                print(CANCEL_DOWNLOAD)
                return None

    def upload(self):
        """
        从客户端用户的家目录上传文件到服务端公共目录中
        :return:
        """
        # 如果家目录为空，打印当前目录没有文件，无法上传
        if not os.listdir(self.hmdir):
            print(NO_FILE)
        else:
            # 列出客户端用户家目录下的所有文件
            self.list_hmdir()
            filename = input(INPUT_UPLOAD_FILE)
            # 如果输入的文件不存在
            hmdir_file = os.path.join(self.hmdir,filename)
            if not os.path.exists(hmdir_file):
                print(NO_UPLOAD_FILE)
            else:
                if User.check_server(filename):
                    # 客户端向服务端发送该文件，获取服务端返回的数据res
                    res = User.socket_client(UPLOAD, hmdir_file, open(hmdir_file, 'rb').read().decode())
                    print(res.decode())
                    # 在服务端写入一条日志
                    self.write_log('uploaded',filename)

    def download(self):
        """
        从服务端公共目录中下载文件到客户端用户的家目录
        :return:
        """
        # 如果公共目录为空，打印当前目录没有文件，无法下载
        if not os.listdir(INVENTORY_DIR):
            print(NO_FILE)
        else:
            # 列出服务端公共目录下的所有文件
            User.list_inventory()
            # 输入要下载的文件名
            filename = input(INPUT_DOWNLOAD_FILE)
            # 如果客户端用户的家目录中已经有同名文件，询问是否覆盖
            hmdir_file = os.path.join(self.hmdir,filename)
            # 如果客户端家目录中不存在同名文件
            if User.check_client(hmdir_file):
                # 客户端向服务端请求该文件，获取服务端返回的文件内容res
                res = User.socket_client(DOWNLOAD,filename)
                if res == NO_FILE_EXIST.encode('utf-8'):
                    print(NO_DOWNLOAD_FILE)
                else:
                    # 将data写入客户端用户的家目录下的文件中
                    open(hmdir_file, 'wb').write(res)
                    print(SUCCESS_DOWNLOAD.format(os.path.relpath(self.hmdir,start='client')))
                    # 在服务端写入一条日志
                    self.write_log('downloaded',filename)

    def list_hmdir(self):
        """
        列出客户端上用户家目录中的文件
        :return:
        """
        # 如果用户家目录为空，打印当前目录没有文件
        if not os.listdir(self.hmdir):
            print(NO_FILE)
        else:
            # # for windows platform
            # cmd = 'dir {0}'.format(self.hmdir)
            # for linux platform
            cmd = 'ls -l {0}'.format(self.hmdir)
            res = os.popen(cmd).read()
            print(HMDIR_CONTENT.format(self.name),end='')
            print(res)

    def show_log(self):
        """
        打印用户操作日志
        :return:
        """
        with open(LOGFILE,'r') as f:
            for line in f:
                print(line,end='')
