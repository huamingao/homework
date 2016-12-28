#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import pickle
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)
DB_DIR = os.path.join(PROJECT_DIR,'db')

from src.user import User
from src.girl import Girl


TYPE = '屌丝'
SEX = '男'

# show()
USER_INFO = '''个人资料一览：
姓名：{0}
年龄：{1}
工作：{2}
国籍：{3}
存款：{4}元
房产：{5}套
车产：{6}辆
技能：'''

# login()
INPUT_NAME = '请输入你在游戏中的名字：'
NAME_NOT_EXIST = '您输入的账号名不存在！注册新玩家请输y,退回初始画面请输q,重新输入请输其他任意键：'
PWD_LOCK = '密码输错达到3次，请联系管理员解锁密码！'
INPUT_PWD = '请输入登录密码：'
LOGIN_SUCCESS = '{0}，欢迎回来！下面继续游戏！'
WRONG_PWD = '您输入的密码有误，请重新输入！'

# register()
REGISTER_NAME = '请设置你在游戏中的名字：'
ALREADY_REGISTER = '您输入的名字已被注册！请重新输入！退出请输q：'
SET_PWD = '请设置登录密码：'
REGISTER_SUCCESS = '{0}，您已注册成功！下面开始游戏！'

#menu()
RULE = '''游戏规则：
1.根据玩家所处年龄段，抽取情景选择题。玩家输入选项编号后，存款、房车等信息将发生变动。
2.每次选择结束后，女神存款增加1000。女神在毕业时傍上高富帅Peter.
3.当玩家存款超过女神，玩家和女神成为恋人。
4.当玩家有车有房存款大于10000，玩家变为高富帅，女神提出成为恋人。
'''
CAMPUS = '大学时，你是一位屌丝，为了赢得女神Liz的心，你决定...'
GRADUATE = '毕业后，Liz傍上了高富帅Peter，你决定...'
YEARS_LATER = '多年后，...'

class Poor(User):

    type = TYPE
    sex = '男'

    def __init__(self,name,password,age=19,job='学生',country='中国',skill=[],money=1000,house=0,car=0):
        self.name = name
        self.password = password
        self.age = age
        self.job = job
        self.country = country
        self.skill = skill
        self.money = money
        self.house = house
        self.car = car
        self.pwdcnt = 0
        self.file = os.path.join(DB_DIR,name)

    def show(self):
        print(USER_INFO.format(self.name,self.age,self.job,self.country,self.money,self.house,self.car),end='')
        for item in self.skill:
            print(item,end=', ')
        print('\n')

    @staticmethod
    def login():
        option = ''
        while option !='q':
            name = input(INPUT_NAME)
            name_file = os.path.join(DB_DIR,name)
            if not os.path.exists(name_file):
                option = input(NAME_NOT_EXIST)
                if option == 'y':
                    Poor.register(name)
                else:
                    continue
            else:
                myobj = pickle.load(open(name_file,'rb'))
                if myobj.pwdcnt > 3:
                    print(PWD_LOCK)
                    return None
                elif myobj.pwdcnt <= 3:
                    pwd = input(INPUT_PWD)
                    if pwd == myobj.password:
                        print(LOGIN_SUCCESS.format(name))
                        myobj.show()
                        myobj.menu()
                    else:
                        print(WRONG_PWD)
                        myobj.pwdcnt += 1
                        pickle.dump(myobj, open(myobj.file, 'wb'))

    @staticmethod
    def register(name=''):
        # 如果传入参数为空，提示用户设置注册名
        if not name:
            option = ''
            while option !='q':
                name = input(REGISTER_NAME)
                if name in os.listdir(DB_DIR):
                    option = input(ALREADY_REGISTER)
                    continue
                else:
                    break
        pwd = input(SET_PWD)
        myobj = Poor(name,pwd)
        pickle.dump(myobj,open(myobj.file,'wb'))
        print(REGISTER_SUCCESS.format(name))
        myobj.show()
        myobj.menu()

    def menu(self):
        print(RULE)
        mygirl = Girl(name='Liz',money=3000)
        if self.age <= 22:
            print(CAMPUS)
        elif 23 <= self.age <= 26:
            print(GRADUATE)
        elif self.age >= 27:
            print(YEARS_LATER)


