#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(PROJECT_DIR,'db')

USER_INFO = '''
***人物资料***
姓名：{0}
年龄：{1}
存款：{2}'''


class User(object):

    def __init__(self,name,password,age=19,money=0):
        self.name = name
        self.password = password
        self.age = age
        self.money = money
        self.file = os.path.join(DB_DIR,name)

    def show(self):
        print(USER_INFO.format(self.name,self.age,self.money))

