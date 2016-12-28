# Author:houyafan
import os, sys,json
BASE_PASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PASH)
from core.data.CONST import BASE_PATH,DATA_PATH
from core.tools.check import *
from core.tools.public_file import *


def admin_user():
    menu_list = ["新增用户","修改额度","冻结账户"]
    for index, item in enumerate(menu_list):
        print('\t\t\t', index, '\t\t\t', item)
    while True:
        menu_type = input("请输入你要选择的功能编号:")
        if check_insert_number(menu_type, menu_list)[0]:
            tmp = check_insert_number(menu_type, menu_list)[1]
            if tmp == 0: # 新增用户
                add_user()
                break
            elif tmp == 1: # 修改额度
                modify_price()
                break
            elif tmp == 2: # "冻结账户"
                block_user()
                break
        else:
            pass


# 新增用户
def add_user():
    while True:
        username = input("请输入你要添加的用户名:")
        passworld = input("请输入你要添加的密码:")
        old_Maxprice = input("请输入你要添加的额度:")
        Maxprice = check_int(old_Maxprice)
        with open(DATA_PATH+"card_message_tmp.json",'r+')as f:
            data=json.load(f)
            if username not in data.keys():
                data[username]={"message":{}}
                data[username]["message"]["password"] = passworld # 密码
                data[username]["message"]["CreditMax"] = Maxprice # 可动额度
                data[username]["message"]["Original"] = Maxprice # 不可动额度
                data[username]["message"]["BankType"] = "Credit" # 卡类型
                data[username]["message"]["status"] = 3  # 账户状态
                data[username]["message"]["Balance"] = 0  # 余额
                write_log(f, data) # 写进card_message_tmp.json
                print("\033[33;1m新增用户成功...\033[0m")
                break
            else:
                print("\033[33;1m您输入的用户已经存在，请确认后重新创建..\033[0m")
                break


# 修改额度
def modify_price():
    while True:
        with open(DATA_PATH+"card_message_tmp.json",'r+')as f:
            data=json.load(f)
            username=input("请输入要调整的用户:")
            if username in data.keys():
                old_modify_money=input("请输入调整的金额:")
                modify_money=check_int(old_modify_money)
                data[username]["message"]["Original"]=modify_money
                write_log(f, data)  # 写进card_message_tmp.json
                print("\033[33;1m修改用户额度成功...\033[0m")
                break
            else:
                print("\033[33;1m您输入的用户不存在，请确认...\033[0m")
                break


# 冻结账户
def block_user():
    while True:
        with open(DATA_PATH+"card_message_tmp.json","r+")as f:
            data=json.load(f)
            username=input("\033[33;1m请输入您要冻结的账户名称:\033[0m")
            if username in data.keys():
                data[username]["message"]["status"] = 2
                write_log(f, data)  # 写进card_message_tmp.json
                print("\033[33;1m%s 已被冻结...\033[0m"% username)
                break
            else:
                print("\033[33;1m您要冻结的账户不存在...\033[0m")
                break