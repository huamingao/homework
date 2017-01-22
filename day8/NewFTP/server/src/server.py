#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import subprocess
import pickle
import socket

from conf.conf import *
from src.user import *


def list_inventory(conn):
    cmd = ' '.join(('ls',INVENTORY_DIR))
    res = os.popen(cmd).read()
    conn.send(res.encode('utf-8'))


def download(conn,name,cmd):
    filename = cmd.replace('download ','')
    file_full_path = os.path.join(INVENTORY_DIR,filename)
    # 检查公共目录中是否存在此文件
    if not os.path.exists(file_full_path):
        conn.send(NO_DOWNLOAD_FILE.encode('utf-8'))
    else:
        # 检查家目录中是否存在此文件
        hmdir_file = os.path.join(USER_HOME_DIR,name,filename)
        if os.path.exists(hmdir_file):
            conn.send(FILE_EXIST_HOME.encode('utf-8'))
        else:
            with open(file_full_path,'rb') as f1:
                content = f1.read()
            with open(hmdir_file,'wb') as f2:
                f2.write(content)
            conn.send(SUCCESS_DOWNLOAD.encode('utf-8'))


def upload(conn,name,cmd):
    filename = cmd.replace('upload ','')
    file_full_path = os.path.join(USER_HOME_DIR,name,filename)
    # 检查家目录中是否存在此文件
    if not os.path.exists(file_full_path):
        conn.send(NO_UPLOAD_FILE.encode('utf-8'))
    else:
        # 检查公共目录中是否存在此文件
        inventory_file = os.path.join(INVENTORY_DIR,filename)
        if os.path.exists(inventory_file):
            conn.send(FILE_EXIST_INVENTORY.encode('utf-8'))
        else:
            with open(file_full_path, 'rb') as f1:
                content = f1.read()
            with open(inventory_file,'wb') as f2:
                f2.write(content)
            conn.send(SUCCESS_UPLOAD.encode('utf-8'))


def overwrite_file_inventory(conn,name,cmd):
    """
    覆盖公共目录中已存在的文件
    """
    filename = cmd.replace('upload ','')
    file_full_path = os.path.join(USER_HOME_DIR,name,filename)
    with open(file_full_path,'rb') as f1:
        content = f1.read()
    with open(os.path.join(INVENTORY_DIR,filename),'wb') as f2:
        f2.write(content)
    conn.send(SUCCESS_UPLOAD.encode('utf-8'))


def overwrite_file_home(conn,name,cmd):
    """
    覆盖家目录中已存在的文件
    """
    filename =cmd.replace('download ','')
    file_full_path = os.path.join(INVENTORY_DIR,filename) 
    with open(file_full_path, 'rb') as f1:
        content = f1.read()
    with open(os.path.join(USER_HOME_DIR,name,filename),'wb') as f2:
        f2.write(content)
    conn.send(SUCCESS_DOWNLOAD.encode('utf-8'))


def login(conn,name,password):
    """
    用户登录：验证服务端用户对象文件中的密码
    :param conn:
    :param name:
    :param password:
    :return:
    """
    user_obj_file = os.path.join(USER_OBJ_DIR,name)
    # 如果用户对象文件不存在，返回用户不存在
    if not os.path.exists(user_obj_file):
        conn.send(NAME_NO_EXIST.encode('utf-8'))
    else:
        user_obj = pickle.load(open(user_obj_file, 'rb'))
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
    # 在服务端创建用户家目录
    os.mkdir(os.path.join(USER_HOME_DIR,name))
    # 在服务端上生成用户对象文件
    with open(os.path.join(USER_OBJ_DIR,name), 'wb') as f:
         pickle.dump(User(name,password), f)
    conn.send(SUCCESS_REGISTER.encode('utf-8'))


def print_home_dir(conn,name):
    """
    转到用户家目录，并打印
    :param conn:
    :param name:
    :return:
    """
    user_home_dir = os.path.join(USER_HOME_DIR,name)
    conn.send(user_home_dir.encode('utf-8'))


def print_inventory_dir(conn):
    conn.send(INVENTORY_DIR.encode('utf-8'))


def run_cmd(conn,name,cmd):
    # 执行自定义命令upload
    if cmd.startswith('upload '):
        upload(conn,name,cmd)
    # 执行自定义命令download
    elif cmd.startswith('download '):
        download(conn,name,cmd)
    # 执行系统命令
    else:
        obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=os.path.join(USER_HOME_DIR,name))
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
    if operation == CHECK_NAME:
        check_name(conn,*data)
    elif operation == REGISTER:
        register(conn,*data)
    elif operation == LOGIN:
        login(conn,*data)
    elif operation == PRINT_HOME_DIR:
        print_home_dir(conn,*data)
    elif operation == PRINT_INVENTORY_DIR:
        print_inventory_dir(conn)
    elif operation == LIST_INVENTORY:
        list_inventory(conn)
    elif operation == OVERWRITE_FILE_INVENTORY:
        overwrite_file_inventory(conn,*data)
    elif operation == OVERWRITE_FILE_HOME:
        print('before overwrite home dir')
        overwrite_file_home(conn,*data)
    # 如果客户端是要执行命令
    elif operation == RUN_CMD:
        run_cmd(conn,*data)

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



