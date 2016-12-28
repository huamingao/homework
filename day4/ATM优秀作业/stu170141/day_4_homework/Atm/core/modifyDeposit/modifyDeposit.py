# Author:houyafan

import json, os, time, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.data.CONST import BASE_PATH, DATA_PATH
from core.login.login import *
from core.tools.public_file import *


# 定义一个通用的装饰器，增加校验登陆的功能
def public(func):
    def common(*args, **kwargs):
        with open(DATA_PATH + "card_message_tmp.json")as f:
            data = json.load(f)
        with open(DATA_PATH + "username.txt","r")as f1:
            abc=f1.read()
        if len(abc)>1:
            username=get_username()
            if data[username]["message"]["status"] == 0:
                func(*args, **kwargs)
            else:
                with open(DATA_PATH + "card_message_tmp.json")as f:
                    data = json.load(f)
                if data[username]["message"]["status"] == 3:  # 状态0为成功 1为失败 2为冻结 3为退出
                    print("请先进行登陆再进行以下操作！")
                    loginAtm()
                    func(*args, **kwargs)
                elif data[username]["message"]["status"] == 2:
                    print("您的银行卡已被冻结，请到营业厅办理解卡！！")
                    exit()
        else:
            loginAtm()
            func(*args, **kwargs)

    return common


# 结算方法
@public
def modify(salary):
    with open(DATA_PATH + 'card_message_tmp.json', 'r+')as f:
        data = json.load(f)
        username = get_username()
        balance = data[username]["message"]["Balance"]  # 余额
        creditmax = data[username]["message"]["CreditMax"]  # 信用额度
        if balance >= salary:  # 余额大于结账的额度
            data[username]["message"]["Balance"] = balance - salary
            write_modify_file(f, data)
            write_modify_bill(salary)
        elif salary > balance > 0:  # 结账的额度大于余额 但余额大于0
            data[username]["message"]["Balance"] = 0
            data[username]["message"]["CreditMax"] = creditmax + balance - salary  # 扣除余额后在走信用额度
            write_modify_file(f, data)
            write_modify_bill(salary)
        elif balance == 0 and salary < creditmax:  # 余额为零 且 结账金额 < 信用额度
            data[username]["message"]["CreditMax"] = creditmax - salary
            write_modify_file(f, data)
            write_modify_bill(salary)
        elif salary > creditmax:  # 结账金额 > 信用额度
            print("\033[31;1m信用卡余额不足，无法购买\033[0m")


# 写入账单
def write_modify_bill(salary):
    with open(DATA_PATH + 'bill.json', 'a+') as f:
        f.seek(0)
        data = json.load(f)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info = '''%s 商店付款 %s 元''' % (new_time, salary)
        public_write(f, info, data)
