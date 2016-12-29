# Author:houyafan
import json, os

from core.tools.check import *

'''校验密码格式'''


def check_username(a, b):
    if len(a) == 0 or len(b) == 0:
        print("\033[32;1m您输入的密码或账号格式不正确，请查正后输入！！\033[0m")
        return True
    else:
        return False


'''校验功能菜单'''


def check_insert_number(insert_parameter, menu_list):
    if insert_parameter.isdigit():
        insert_parameter = int(insert_parameter)
        if 0 <= insert_parameter < len(menu_list):
            if menu_list[insert_parameter] not in menu_list:
                print('\033[31;1m输入的功能编号有误，请重新输入要操作的功能:\033[0m')
                return False, ''
            return True, insert_parameter
        else:
            print('\033[31;1m输入的功能编号有误，请重新输入要操作的功能:\033[0m')

            return False, ''
    else:
        print('\033[31;1m输入的功能编号有误，请重新输入要操作的功能:\033[0m')
        return False, ''


'''校验是否已登录'''


def check_login_studus():
    if os.path.exists('login_status'):
        with open('login_status', 'r') as f:
            data = json.load(f)
        if data["status"] == "成功":
            return True
        elif data["status"] == "失败":
            return False
        else:
            exit("您的银行卡已被锁死，请到营业厅办理解卡！！")
            return False
    else:
        return False


'''校验金额类型,同时转为金额类型'''


def check_money(money):
    if money.isdigit():
        info='''%s.00'''%money
        money=float(info)
        return money
    elif money.count('.') == 1:
        money = float(money)
        return money


'''字符串转整型'''


def check_int(string):
    if string.isdigit():
        string = int(string)
    return string
