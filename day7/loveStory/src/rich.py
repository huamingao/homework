#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(PROJECT_DIR,'db')

from src.user import User


USER_INFO = '''
***{0}人物资料***
姓名：{1}
年龄：{2}
工作：{3}
国籍：{4}
存款：{5}元
房产：{6}套
车产：{7}辆'''

TYPE = '高富帅'
SEX = '男'
JOB = 'CEO'
COUNTRY = '美国'

class Rich(User):

    type = TYPE
    sex = '男'
    job = JOB
    country = COUNTRY

    def __init__(self,name,age=19,money=10000,house=1,car=1):
        self.name = name
        self.age = age
        self.money = money
        self.house = house
        self.car = car
        self.file = os.path.join(DB_DIR,name)


    def show(self):
        print(USER_INFO.format(Rich.TYPE,self.name,self.age,Rich.job,Rich.country,self.money,self.house,self.car))