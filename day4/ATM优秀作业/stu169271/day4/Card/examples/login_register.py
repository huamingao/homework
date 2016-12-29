#!/usr/bin/env python
# encoding: utf-8



import os
import pickle
import datetime

login_log = "login.log"
password_file = "password.txt"
lock_file = "lock_account.txt"
user_info_file = "user_info.pickle"
color_end = "\033[0m"
color_red = "\033[31;1m"
color_green = "\033[32;1m"
today = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
LOGIN_USER = {"is_login": False}


def file_is_exist(filename):
    if os.path.exists(filename):
        message = "True"
    else:
        message = "False"
    return message


def check_login(func):
    """
    装饰器函数：验证是否完成登录
    :param func: 要装饰的函数
    :return:
    """
    def inner(*args, **kwargs):
        # print(LOGIN_USER['is_login'])
        if LOGIN_USER['is_login']:
            r = func()
            return r
        else:
            print(color_red + "你还未登录，请登录" + color_end)
    return inner


def check_user_level(func):
    """
    装饰器函数：验证用户等级 0 普通用户 1 管理员
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        # print(LOGIN_USER['user_level'])
        # print(LOGIN_USER['user_level'] == "1")
        if LOGIN_USER['user_level'] == 1:
            r = func()
            return r
        else:
            print(color_red + "需要管理员权限" + color_end)
    return inner


def login(username, account_name, password):
    """
    验证用户登录
    :param username: 接受用户的姓名
    :param account_name: 接受用户的登录账号
    :param password: 接受用户的登录密码
    :return:
    """
    res = file_is_exist(lock_file)   # 判断用户锁文件是否存在，不存在创建
    if res == "False":
        open(lock_file, "w+").close()

    count = 0
    flag = True
    while flag:
        if count < 3:                           # 只要重试不超过三次就不断循环
            with open(lock_file, 'r') as pas:   # 判断账号是否在锁定列表中，如果已经被锁定过，直接退出程序
                for line in pas.readlines():
                    if username in line:
                        print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
                        flag = False
                        break
            '''
              判断账号及密码是否在password.txt文件中存在且正确，如果正确记录日志，输出登录信息
            '''
            card_user_info_dict = pickle.load(open(user_info_file, 'rb'))
            user_name = card_user_info_dict[username]['account_name']
            pass_word = card_user_info_dict[username]['password']
            agree_flag = card_user_info_dict[username]['agree_flag']

            if account_name == user_name and password == pass_word and agree_flag == 1:
                print(color_green + "欢迎 %s,登陆成功  !!!" % username + color_end)
                LOGIN_USER['is_login'] = True
                LOGIN_USER['current_user'] = user_name
                LOGIN_USER['user_level'] = 0    # 设置用户等级 0 普通用户 1 管理员
                flag = False        			# 如果账号及密码信息正确，则记录日志，跳出循环
                break
            elif account_name == 'admin' and password == '123':
                print(color_green + "欢迎管理员登陆成功  !!!" + color_end)
                LOGIN_USER['user_level'] = 1
            else:
                print("账号密码错误或者账号未激活")
                continue
                count += 1
            # 如果同一个账号连续输错三次，则将账号记录到锁定文件列表，并退出程序
        else:
            print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
            flag = False


def card_register_user():
    """
    信用卡申请功能
    :return:
    """
    res = file_is_exist(user_info_file)
    if res == "False":
        card_user_info_dict = {}
        pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))
    else:
        card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取原有的用户信息

    card_user_info = {}
    # card_user_info_dict = {}
    user_name = input("姓名：")
    email = input("E-mail：")
    phone_number = input("手 机 号：")
    area_info = input("地区信息：")
    account_name = input("设置登录账号(审批通过生效)：")
    password = input("设置登录密码(审批通过生效)：")
    card_user_info["user_name"] = user_name
    card_user_info["email"] = email
    card_user_info["phone_number"] = phone_number
    card_user_info["area_info"] = area_info
    card_user_info["agree_flag"] = 0                # 0 未审批 1 审批完成
    card_user_info["agree_register"] = 0            # 0 审批失败 1 审批成功
    card_user_info["card_limit"] = 0                # 默认额度为0，审批通过然后进行额度授权
    card_user_info["account_name"] = account_name   # 信用卡登录账号 审批通过后生效
    card_user_info["password"] = password           # 信用卡登录密码 审批通过后生效
    card_user_info_dict[user_name] = card_user_info

    pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))
    print(color_green + "信用卡申请信息已经提交，请耐心等待审批结果....." + color_end)

