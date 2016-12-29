# Author:houyafan
import os, sys, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.modifyDeposit.modifyDeposit import *
from core.data.CONST import BASE_PATH, DATA_PATH
from core.tools.check import *
from core.tools.public_file import *


# 取现方法
@public
def takeMoney():
    with open(DATA_PATH + "card_message_tmp.json", "r+")as f:
        data = json.load(f)
        username = get_username()
        take_money = input("\033[33;1m请输入要取现的金额:\033[0m")
        new_take_money = check_int(take_money)  # 取现金额
        max_take_money = int(data[username]["message"]["Original"] / 2)  # 最大取现金额
        balance = data[username]["message"]["Balance"]  # 余额
        creditmax = data[username]["message"]["CreditMax"]  # 剩余信用额度
        procedure = int(new_take_money * 0.05)  # 手续费
        if new_take_money - balance > max_take_money:  # 控制它 不能取现超限
            print("您最多能取现信用额度的50%,您的信用额度是\033[31;1m{a}\033[0m元,最大取现额度是\033[31;1m{b}\033[0m元". \
                  format(a=data[username]["message"]["Original"], b=max_take_money))
        elif new_take_money == balance:  # 取现 == 余额
            data[username]["message"]["Balance"] = 0
            data[username]["message"]["CreditMax"] = creditmax - procedure
            write_take_money(f, data, procedure)
            write_take_bill(new_take_money, procedure)  # 写入账单
        elif new_take_money > balance:
            data[username]["message"]["Balance"] = 0
            data[username]["message"]["CreditMax"] = creditmax - procedure - (new_take_money - balance)
            write_take_money(f, data, procedure)
            write_take_bill(new_take_money, procedure)  # 写入账单
        elif new_take_money < balance:
            if procedure > balance - new_take_money:  # 手续费>余额-取现金额
                data[username]["message"]["Balance"] = 0
                data[username]["message"]["CreditMax"] = creditmax - procedure - (balance - new_take_money)
                write_take_money(f, data, procedure)
                write_take_bill(new_take_money, procedure)  # 写入账单
            elif procedure == balance - new_take_money:  # 手续费=余额-取现金额
                data[username]["message"]["Balance"] = 0
                write_take_money(f, data, procedure)
                write_take_bill(new_take_money, procedure)  # 写入账单
            elif procedure < balance - new_take_money:  # 手续费<余额-取现金额
                data[username]["message"]["Balance"] = balance - procedure - new_take_money
                write_take_money(f, data, procedure)
                write_take_bill(new_take_money, procedure)  # 写入账单
        elif balance == 0:
            data[username]["message"]["CreditMax"] = creditmax - procedure - new_take_money
            write_take_money(f, data, procedure)
            write_take_bill(new_take_money, procedure)  # 写入账单


# 写入账单
def write_take_bill(new_take_money, procedure):
    with open(DATA_PATH + 'bill.json', 'a+') as f:
        f.seek(0)
        data = json.load(f)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info = '''%s 提现 %s 元，手续费 %s 元''' % (new_time, new_take_money, procedure)
        public_write(f, info, data)
