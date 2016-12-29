#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import socket
import time
import os

# 定义当前目录
current_dir = os.getcwd()


# 定义一个类
class EddyFtpserver(SocketServer.BaseRequestHandler):
    # 定义接收文件方法
    def recvfile(self, filename):
        print
        "starting reve file!"
        f = open(filename, 'wb')
        self.request.send('ready')
        while True:
            data = self.request.recv(4096)
            if data == 'EOF':
                print
                "recv file success!"
                break
            f.write(data)
        f.close()
        # 定义放送文件方法

    def sendfile(self, filename):
        print
        "starting send file!"
        self.request.send('ready')
        time.sleep(1)
        f = open(filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.request.sendall(data)
        f.close()
        time.sleep(1)
        self.request.send('EOF')
        print
        "send file success!"

    # SocketServer的一个方法
    def handle(self):
        print
        "get connection from :", self.client_address
        while True:
            try:
                data = self.request.recv(4096)
                print
                "get data:", data
                if not data:
                    print
                    "break the connection!"
                    break
                else:
                    action, filename = data.split()
                    # 判断上传
                    if action == "put":
                        # 上传文件保存到当前目录下
                        filename = current_dir + '/' + os.path.split(filename)[1]
                        self.recvfile(filename)
                        # 判断下载
                    elif action == 'get':
                        self.sendfile(filename)
                    else:
                        print
                        "get error!"
                        continue
            except Exception, e:
                print
                "get error at:", e


if __name__ == "__main__":
    host = 'localhost'
    port = 8888
    # 实例化
    s = SocketServer.ThreadingTCPServer((host, port), EddyFtpserver)
    s.serve_forever()

客户端
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-23 23:24:53
# @Author  : eddy (278298125@qq.com)
# @Link    : http://my.oschina.net/eddylinux
# @Version : 1.0

import socket
import time
import os

ip = 'localhost'
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 定义当前目录
current_dir = os.getcwd()


def recvfile(filename):
    print
    filename
    print
    "server ready, now client rece file~~"
    f = open(filename, 'wb')
    while True:
        data = s.recv(4096)
        if data == 'EOF':
            print
            "recv file success!"
            break
        f.write(data)
    f.close()


def sendfile(filename):
    print
    "server ready, now client sending file~~"
    f = open(filename, 'rb')
    while True:
        data = f.read(4096)
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(1)
    s.sendall('EOF')
    print
    "send file success!"


def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True


try:
    s.connect((ip, port))
    while 1:
        client_command = raw_input(">>")
        if not client_command:
            continue

        action, filename = client_command.split()
        if action == 'put':
            if confirm(s, client_command):
                sendfile(filename)
            else:
                print
                "server get error!"
        elif action == 'get':
            if confirm(s, client_command):
                print
                current_dir
                print
                filename
                filename = current_dir + '/' + os.path.split(client_command)[1]
                print
                filename
                recvfile(filename)
            else:
                print
                "server get error!"
        else:
            print
            "command error!"
except socket.error, e:
    print
    "get error as", e
finally:
    s.close()