#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
import json
import random
import datetime
import time
import shutil

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DB = os.path.join(PROJECT_DIR,'db')

from src import crontab as src_crontab
from src import admin as src_admin
from src import client as src_client
from lib import validator

CURRENT_USER_INFO = {'is_authenticated':False,'username':''}

# main函数（管理员入口）中用到的交互文字
MAIN_MENU = """
欢迎来到管理员后台
1、管理员登录
2、创建账户
3、删除账户
4、冻结账户
5、修改额度
6、查询账户
退出并注销，请输q
"""
LOGOFF_MSG = '{username} 您已成功退出'
OPTION_PROMPT = '请输入您的选项：'
INVALID_MSG = '您的输入不合法，请重新输入！'
SUCCESS_LOGIN = '\033[31;1m{username}，您已成功登陆后台管理系统！\033[0m'
EXIT_MSG = '\033[31;1m您已成功退出当前画面\033[0m'
AUTO_JUMP_BACK = '系统为您自动跳转到上一个画面...请按提示继续操作'
INPUT_TO_CONTINUE = '\033[31;1m若要继续操作，请输任意键\033[0m'

# login函数中用到的交互文字
LOGIN_MSG = '\033[31;1m您尚未以管理员身份登录！请按下面提示登录，若要中途退出，请输q：\033[0m'
INPUT_USERNAME = '管理员登录，请输用户名；：'
INPUT_PASSWORD = '请输入管理员密码：'
NO_EXIST_CARD = '\033[31;1m您输入的卡号不存在！\033[0m'

# create_user函数中用到的交互文字
INPUT_INFO_MSG = """
您已选择创建账户，请按下面提示输入相应信息。若要中途退出，请输q：
系统已自动生成信用卡卡号：{card_num}
"""
INPUT_CARD_NUM = '请输入要操作的信用卡卡号,若要中途退出，请输q：'
INPUT_CARD_USERNAME = '请输入持卡人姓名：'
INPUT_INIT_PASSWORD = '请输入初始密码：'
INPUT_CREDIT = '请输入信用卡额度：'
NO_EXIST_USER = '\033[31;1m您输入的用户名不存在！请重新输入！\033[0m'
PWD_INVALID = '\033[31;1m密码错误，请重新输入用户名和密码！\033[0m'
SUCCESS_CREATE_USER = '\n您已成功创建账户如下：'
CARD_INFO = """
信用卡号：{card_num}
持卡人姓名：{username}
刷卡密码：{password}
信用卡额度：{credit}
当前可用额度：{balance}
当前储蓄金额：{savings}
卡片状态：{status}
发卡时间（账单日）：{enroll_date}
过期时间：{expire_date}
欠款记录：无"""
NORMAL = '正常'

# lock_user函数中用到的交互文字
LOCKED_MSG = '无法冻结账户！账户当前状态已经是冻结！'
SET_LOCK_USER = '您已成功修改[卡号{card_num}，持卡人{username}]的账户状态，当前状态为冻结'
VERIFY_LOCK = '确认要冻结该账户？确认请输非q的任意键；放弃冻结，请输q：'

# set_credit函数中用到的交互文字
CURRENT_CREDIT_MSG = '[卡号{card_num}，持卡人{username}]的当前信用额度为{credit}，当前可用额度{balance}'
SUCCESS_SET_CREDIT = '您已成功修改[卡号{card_num}，持卡人{username}]的信用额度，当前信用额度为{credit},，当前可用额度{balance}'


# remove_user函数中用到的交互文字
CURRENT_CARD_MSG = '您正在操作的账户信息如下：'
VERIFY_REMOVE = '确认要删除该账户？确认请输非q的任意键；放弃删除，请输q：'
SUCCESS_REMOVE_USER = '您已成功删除账户：[卡号{card_num}]'


def login():
    """
    登录
    :return:
    """
    if CURRENT_USER_INFO['is_authenticated']:
        print(SUCCESS_LOGIN.format(username=CURRENT_USER_INFO['username']))
        print(AUTO_JUMP_BACK)
        return True
    else:
        print(LOGIN_MSG)
        while True:
            username = input(INPUT_USERNAME)
            if username == 'q':
                print(EXIT_MSG,AUTO_JUMP_BACK)
                main()
            if username not in os.listdir(PROJECT_DB):
                print(NO_EXIST_USER)
            else:
                userinfo_file = os.path.join(PROJECT_DB,username,'userinfo')
                userinfo_dict = json.load(open(userinfo_file,'r'))
                if userinfo_dict['user_type'] == 'user':
                    print('{username},您输入的是普通用户信用卡卡号，为您自动跳转到普通用户自助平台'.format(username=userinfo_dict['username']))
                    src_client.main()
                else:
                    password = input(INPUT_PASSWORD)
                    if password == 'q':
                        print(EXIT_MSG, AUTO_JUMP_BACK)
                        main()
                    if password != userinfo_dict['password']:
                        print(PWD_INVALID)
                    else:
                        CURRENT_USER_INFO['username'] = username
                        CURRENT_USER_INFO['is_authenticated'] = True
                        print(SUCCESS_LOGIN.format(username = userinfo_dict['username']))
                        print(AUTO_JUMP_BACK)
                        return None



def outer(func):
    """
    装饰器，在执行任何其他函数之前先执行login函数
    :param func:
    :return:
    """
    def inner(*args,**kwargs):
        if not CURRENT_USER_INFO['is_authenticated']:
            login()
        return func(*args,**kwargs)
    return inner


@outer
def create_user():
    # 生成卡号，前两位是00，后4位是随机数
    random_num = random.randrange(1000,9999)
    card_num = '00' + str(random_num)
    # 为该卡创建文件目录结构
    os.makedirs(os.path.join(PROJECT_DB,card_num,'record'))
    print(INPUT_INFO_MSG.format(card_num=card_num),end='')
    # 提示用户输入信息
    username = input(INPUT_CARD_USERNAME)
    if username == 'q':
        os.removedirs(os.path.join(PROJECT_DB, card_num, 'record'))
        return 'q'
    password = input(INPUT_INIT_PASSWORD)
    if password == 'q':
        os.removedirs(os.path.join(PROJECT_DB, card_num, 'record'))
        return 'q'
    credit = balance = validator.force_digit(INPUT_CREDIT, INVALID_MSG)
    if credit =='q':
        os.removedirs(os.path.join(PROJECT_DB, card_num, 'record'))
        return 'q'
    enroll_date = datetime.date.today()
    enroll_date_timestamp = time.time()
    expire_date = enroll_date + datetime.timedelta(days=365*4)
    expire_date.timetuple()
    expire_date_timestamp = time.mktime(expire_date.timetuple())
    print(SUCCESS_CREATE_USER)
    print(CARD_INFO.format(card_num=card_num,username=username,password=password,credit=credit,balance=balance,
                           savings=0,enroll_date=enroll_date,expire_date=expire_date,status=NORMAL))
    base_info = {'card_num':card_num,
                 'user_type':'user',  # 用户类型
                 'username':username,
                 'password':password,
                 'credit':credit,   # 信用卡额度
                 'balance':balance, #当前可用额度
                 'savings':0,   # 储蓄金额
                 'enroll_date':enroll_date_timestamp,   # 还款日
                 'expire_date':expire_date_timestamp,    # 信用卡过期时间
                 'status':0,
                 'debt':[]   # 欠款记录，如：[{'date':'201609' ,'month_debt':8000,'status':'already billed'},{'date':'201605','month_debt':5000,'status':'pending billing'}]
                 }
    json.dump(base_info,open(os.path.join(PROJECT_DB,card_num,'userinfo'),'w'))


@outer
def remove_user():
    card_num = src_client.print_user()
    if card_num == 'q':
        return 'q'
    user_dir = os.path.join(PROJECT_DB, card_num)
    if input(VERIFY_REMOVE) == 'q':
        return 'q'
    else:
        shutil.rmtree(user_dir)
        print(SUCCESS_REMOVE_USER.format(card_num=card_num))


@outer
def lock_user():
    card_num = src_client.print_user()
    if card_num == 'q':
        return 'q'
    user_file = os.path.join(PROJECT_DB, card_num,'userinfo')
    base_info = json.load(open(user_file,'r'))
    if base_info['status'] == 1:
        print(LOCKED_MSG)
        input(INPUT_TO_CONTINUE)
        return 'q'
    elif base_info['status'] == 0:
        if input(VERIFY_LOCK) == 'q':
            return 'q'
        else:
            base_info['status'] = 1
            json.dump(base_info, open(user_file, 'w'))
            print(SET_LOCK_USER.format(card_num = base_info['card_num'],username = base_info['username']))


@outer
def set_credit():
    while True:
        card_num = input(INPUT_CARD_NUM)
        if card_num == 'q':
            return 'q'
        user_file = os.path.join(PROJECT_DB, card_num, 'userinfo')
        if not os.path.exists(user_file):
            print(NO_EXIST_CARD)
        else:
            base_info = json.load(open(user_file, 'r'))
            print(CURRENT_CREDIT_MSG.format(card_num=base_info['card_num'],username=base_info['username'],credit=base_info['credit'],balance=base_info['balance']))
            credit = validator.force_digit(INPUT_CREDIT, INVALID_MSG)
            if credit == 'q':
                return 'q'
            base_info['balance'] = credit - (base_info['credit'] - base_info['balance'])
            base_info['credit'] = credit
            json.dump(base_info, open(user_file, 'w'))
            print(SUCCESS_SET_CREDIT.format(card_num = base_info['card_num'],username = base_info['username'],credit = base_info['credit'],balance=base_info['balance']))
            return None


def main():
    ret = True
    while True:
        # 若ret为False，说明当前操作没有正常完成，提示“您已中断当前操作”
        if ret == 'q':
            print(EXIT_MSG,AUTO_JUMP_BACK)
        elif not ret:
            input(INPUT_TO_CONTINUE)
        print(MAIN_MENU)
        option = input(OPTION_PROMPT)
        if option == 'q':
            print(LOGOFF_MSG.format(username = CURRENT_USER_INFO['username']))
            CURRENT_USER_INFO['is_authenticated'] = False
            src_crontab.main()
        if option == '1':
            ret = login()
        elif option == '2':
            ret = create_user()
        elif option == '3':
            ret = remove_user()
        elif option == '4':
            ret = lock_user()
        elif option == '5':
            ret = set_credit()
        elif option == '6':
            if not CURRENT_USER_INFO['is_authenticated']:
                ret = login()
            if CURRENT_USER_INFO['is_authenticated']:
                ret = src_client.print_user()
                if ret != 'q':
                    ret = None
        else:
            print(INVALID_MSG)
            ret = None
