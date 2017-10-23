#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import subprocess
import pickle
import socket
import os

from conf.conf import *
from src.user import *


def download(conn,filename):
    # 如果公共目录中不存在此文件，返回文件不存在
    if not os.path.exists(os.path.join(INVENTORY_DIR,filename)):
        conn.send(NO_DOWNLOAD_FILE.encode('utf-8'))
    # 否则返回文件内容
    else:
        with open(os.path.join(INVENTORY_DIR,filename), 'rb') as f:
            res = f.read()
        conn.send(res)


def upload(conn,filename,content):
    # 检查公共目录中是否存在此文件
    if os.path.exists(os.path.join(INVENTORY_DIR,filename)):
        conn.send(FILE_EXIST_INVENTORY.encode('utf-8'))
    else:
        with open(os.path.join(INVENTORY_DIR, filename), 'wb') as f:
            f.write(content.encode('utf-8'))
        conn.send(SUCCESS_UPLOAD.encode('utf-8'))


def login(conn,name,password):
    """
    用户登录：验证服务端用户对象文件中的密码
    :param conn:
    :param name:
    :param password:
    :return:
    """
    # 如果用户对象文件不存在，返回用户不存在
    if not os.path.exists(os.path.join(USER_OBJ_DIR,name)):
        conn.send(NAME_NO_EXIST.encode('utf-8'))
    else:
        user_obj = pickle.load(open(os.path.join(USER_OBJ_DIR,name), 'rb'))
        # 如果密码不正确，返回密码错误
        if password != user_obj.password:
            conn.send(INVALID_PWD.encode('utf-8'))
        # 如果密码正确，返回成功登录
        else:
            conn.send(SUCCESS_LOGIN.encode('utf-8'))


def register(conn,name,password):
    """
    注册新用户
    :param conn:
    :param name:
    :param password:
    :return:
    """
    if os.path.exists(os.path.join(USER_OBJ_DIR,name)):
        conn.send(NAME_EXIST.encode('utf-8'))
    else:
        # 在服务端上生成用户对象文件
        with open(os.path.join(USER_OBJ_DIR,name), 'wb') as f:
             pickle.dump(User(name,password), f)
        conn.send(SUCCESS_REGISTER.encode('utf-8'))


def list_inventory(conn):
    """
    响应请求：打印公共目录文件列表
    :param conn:
    :return:
    """
    # for windows
    cmd = 'dir {0}'.format(INVENTORY_DIR)
    # # for linux
    # cmd = 'ls -l {0}'.format(INVENTORY_DIR)
    obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = obj.communicate()
    if stdout:
        conn.send(stdout)
    if stderr:
        conn.send(stderr)


def run_cmd_on_server(conn,cmd):
    obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=INVENTORY_DIR)
    stdout,stderr = obj.communicate()
    if stdout:
        conn.send(stdout)
    elif stderr:
        conn.send(stderr)
    else:
        conn.send(SUCCESS_RUN_CMD.encode('utf-8'))


def handle_request(conn,data):
    """
    处理客户端向服务端发出的请求
    :param conn: 服务端到客户端的连接实例
    :param data: 客户端向服务端发送的信息
    :return:
    """
    ops_data = data.decode().split('+')
    operation, data = ops_data[0],ops_data[1:]
    if operation == REGISTER:
        register(conn,*data)
    elif operation == LOGIN:
        login(conn,*data)
    elif operation == LIST:
       list_inventory(conn)
    elif operation == UPLOAD:
        upload(conn,*data)
    elif operation == DOWNLOAD:
        download(conn,*data)
    elif operation == RUN_CMD:
        run_cmd_on_server(conn,*data)


def server_socket():
    # 在服务端创建一个socket对象
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 服务端绑定要监听的端口6969
    server.bind(SERVER_ADDR)
    # 服务端开始监听
    server.listen()
    print(START_LISTEN)
    while True:
        # 创建服务端到客户端的连接实例
        conn, addr = server.accept()
        # 服务端接收来自客户端的请求
        data = conn.recv(1024)
        # 服务端处理来自客户端的请求
        handle_request(conn,data)
        print(COMPLETE_REQUEST)
        # 结束连接
        conn.close()
        print(CLOSE_COON)



