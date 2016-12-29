#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


# socket服务端

import socket
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from lib import logger

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_DIR = os.path.join(PROJECT_DIR, 'db','server', 'inventory')
SERVER_ADDR = ('localhost', 6969)
LOGFILE = os.path.join(PROJECT_DIR,'db','server','log')

START_LISTEN = '服务端开始监听了！'
ESTABLISH_CONN = '服务端已经与客户端建立连接'
REC_FROM_CLIENT = '服务端正在接收客户端传来的数据...'
SEND_CLIENT_FILE = '服务端正在向给客户端发送文件...'
REC_CLIENT_FILE = '服务端正在接收客户端发来的文件...'
SEND_CLIENT_RES = '服务端执行了系统命令，正在向客户端发送执行结果...'
COMPLETE_REQUEST = '客户端请求处理完毕！即将关闭本次连接..'
CLOSE_COON = '本次连接已关闭!'
SUCCESS_UPLOAD = '文件已成功上传到服务端公共目录'
CANCEL_UPLOAD = '您已取消上传文件！'
NO_FILE_EXIST = '文件不存在'
FILE_EXIST = '服务端已存在同名文件，是否覆盖？y/n:'
READY_GET_UPLOAD = '服务端已准备好接收客户端的上传'
SUCCESS_LOGOFF = '您已成功注销登录'

RUN_CMD = '我要执行系统命令'
DOWNLOAD = '我要下载'
PREPARE_UPLOAD = '预备上传'
UPLOAD = '我要上传'
LOGOFF = '注销登录'
WRITE_LOG = '写日志'


def resp_list_inventory(conn,cmd):
    """
    服务端响应客户端传来的系统命令，返回执行结果给客户端
    :param conn: 服务端到客户端的连接实例
    :param cmd: 要执行的系统命令
    :return:
    """
    if os.system(cmd) == 0:
        res = os.popen(cmd).read()
        print(SEND_CLIENT_RES)
        conn.send(res.encode('utf-8'))


def resp_download(conn,filename):
    """
    服务端响应客户端的下载请求
    :param conn: 服务端到客户端的连接实例
    :param filename: 要下载的文件名
    :return:
    """
    inventory_file = os.path.join(INVENTORY_DIR,filename)
    # 如果输入的文件在公共目录中不存在
    if not os.path.exists(inventory_file):
        conn.send(NO_FILE_EXIST.encode('utf-8'))
    else:
        res = open(inventory_file,'rb').read()
        print(SEND_CLIENT_FILE)
        conn.sendall(res)


def resp_check_server(conn,filename):
    """
    服务端响应客户端预备上传的请求，检查服务端是否存在同名文件
    :param conn:
    :param filename:
    :return:
    """
    inventory_file = os.path.join(INVENTORY_DIR, filename)
    if os.path.exists(inventory_file):
        conn.send(FILE_EXIST.encode('utf-8'))
    else:
        conn.send(READY_GET_UPLOAD.encode('utf-8'))


def resp_upload(conn,filename,content):
    """
    服务端响应客户端的上传请求
    :param conn: 服务端到客户端的连接实例
    :param filename: 要上传的文件名
    :param content: 要上传的文件内容
    :return:
    """
    inventory_file = os.path.join(INVENTORY_DIR,filename)
    open(inventory_file,'wb').write(content.encode('utf-8'))
    print(REC_CLIENT_FILE)
    conn.send(SUCCESS_UPLOAD.encode('utf-8'))


def resp_logoff(conn):
    """
    服务端响应客户端的注销请求
    :param conn:
    :return:
    """
    conn.send(SUCCESS_LOGOFF.encode('utf-8'))


def handle_request(conn,data):
    """
    处理客户端向服务端发出的请求
    :param conn: 服务端到客户端的连接实例
    :param data: 客户端向服务端发送的信息
    :return:
    """
    ops_data = data.decode().split('+')
    if len(ops_data) == 2:
        operation, data = ops_data
    elif len(ops_data) == 3:
        operation,filename,content = ops_data
    # 如果客户端是要执行系统命令
    if operation == RUN_CMD:
        resp_list_inventory(conn,data)
    # 如果客户端是要下载
    elif operation == DOWNLOAD:
        resp_download(conn,data)
    # 如果客户端是要上传
    elif operation == PREPARE_UPLOAD:
        resp_check_server(conn,data)
    elif operation == UPLOAD :
        resp_upload(conn,filename,content)
    elif operation == LOGOFF:
        logger.logger(LOGFILE,data)
        resp_logoff(conn)
    elif operation == WRITE_LOG:
        # 在服务端写入一条日志
        logger.logger(LOGFILE,data)


def main():
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
        print(ESTABLISH_CONN)
        # 服务端接收来自客户端的请求
        print(REC_FROM_CLIENT)
        data = conn.recv(1024)
        # 服务端处理来自客户端的请求
        handle_request(conn,data)
        print(COMPLETE_REQUEST)
        # 结束连接
        conn.close()
        print(CLOSE_COON)


if __name__ == '__main__':
    main()
