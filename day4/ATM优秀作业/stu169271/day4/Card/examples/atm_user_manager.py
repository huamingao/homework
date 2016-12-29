#!/usr/bin/env python
# encoding: utf-8



import pickle
import datetime
from login_register import *

user_info_file = "user_info.pickle"
color_end = "\033[0m"
color_red = "\033[31;1m"
color_green = "\033[32;1m"
today = datetime.datetime.today().strftime("%Y%m%d%H%M%S")



@check_login
@check_user_level
def audit_user_register():
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取原有的用户信息
    print("已经有的申请信息(审批状态：0 未审批 1 审批完成 )：")
    for i in card_user_info_dict.keys():
        user_info_msg = """
姓名：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%s
        """ % (card_user_info_dict[i]['user_name'],
               card_user_info_dict[i]['phone_number'],
               card_user_info_dict[i]['email'],
               card_user_info_dict[i]['area_info'],
               card_user_info_dict[i]['agree_flag'],
               card_user_info_dict[i]['card_limit'],)
        print(user_info_msg.strip("\n"))
    while True:
        card_user_agree = input("请选择用户进行审批(q 退出)：")
        if card_user_agree == "q" or card_user_agree == "quit":
            break
        else:
            for i in card_user_info_dict.keys():
                if card_user_agree == card_user_info_dict[i]['user_name']:
                    user_info_msg = """
 姓名：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%s
                            """ % (card_user_info_dict[i]['user_name'],
                                   card_user_info_dict[i]['phone_number'],
                                   card_user_info_dict[i]['email'],
                                   card_user_info_dict[i]['area_info'],
                                   card_user_info_dict[i]['agree_flag'],
                                   card_user_info_dict[i]['card_limit'],)
                    print(user_info_msg.strip("\n"))

        card_agree = input("是否同意该用户申请(y/n):")
        if card_agree == "yes" or card_agree == "y":
            card_user_info_dict[card_user_agree]['agree_flag'] = 1
        else:
            break

        card_agree_limit = input("请输入授权额度：")
        card_user_info_dict[card_user_agree]['card_limit'] = card_agree_limit
        pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件

        for i in card_user_info_dict.keys():
            user_info_msg = """
姓名：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%s
                    """ % (card_user_info_dict[i]['user_name'],
                           card_user_info_dict[i]['phone_number'],
                           card_user_info_dict[i]['email'],
                           card_user_info_dict[i]['area_info'],
                           card_user_info_dict[i]['agree_flag'],
                           card_user_info_dict[i]['card_limit'],)
            print(user_info_msg.strip("\n"))


def card_limit_manager():
    pass


def frozen_account_manager():
    pass


def atm_user_manager_menu():
    while True:
        msg_01 = """
=========================================
            欢迎登陆xx信用卡中心
=========================================
    01、审批用户申请(审批并授权用户额度)
    02、用户额度管理
    03、冻结账号
    04、退出
=========================================
"""
        print(msg_01)
        choice_num = input("请选择：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            audit_user_register()
        elif choice_num == 2:
            pass
        elif choice_num == 3:
            pass
        else:
            break


