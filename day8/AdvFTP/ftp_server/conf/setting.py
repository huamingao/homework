#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os, sys

# 加密用户使用的密钥,用户可以自行更改
PASSWORD_KEY = "123456"

# 项目工作目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 服务端的IP、端口
HOST,PORT = 'localhost',5555

# 所有用户的家目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data')

# 所有用户对象的json文件
USERS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'users')
