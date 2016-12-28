# Author:houyafan
import json, os, time, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.data.CONST import BASE_PATH, DATA_PATH
from core.tools.public_file import *
from core.tools.check import *


# 转账
def turn_price():
    with open(DATA_PATH + "card_message_tmp.json", 'r+')as f:
        data=json.load(f)
        old_price=input("\033[33;1m请输入你要转账的金额:\033[0m")
        price=check_int(old_price)
        username=get_username()
        turn_username=input("\033[33;1m请输入你要转账的用户名:\033[0m")
        balance=data[username]["message"]["Balance"]
        if username == turn_username:
            print("\033[31;1m不能转账给自己，请确认你的操作..\033[0m")
        else:
            if turn_username in data.keys(): # 转账用户在user中
                if balance > price: # 余额 > 转账金额
                    data[username]["message"]["Balance"]=balance - price
                    data[turn_username]["message"]["Balance"]=balance + price
                    write_turn_money(f, data, turn_username, price)
                    write_turn_bill(turn_username, price)
                elif balance== price: # 余额 = 转账金额
                    data[username]["message"]["Balance"] = 0
                    data[turn_username]["message"]["Balance"] = balance + price
                    write_turn_money(f, data, turn_username, price)
                    write_turn_bill(turn_username, price)
                else:
                    print("\033[31;1m您的余额已不足转款,请充值后转账...\033[0m")
            else:
                print("\033[31;1m您要转账的用户尚未注册，请查证后重新转账...\033[0m")

# 写入账单
def write_turn_bill(turn_username,price):
    username = get_username()
    with open(DATA_PATH + 'bill.json', 'a+') as f:
        f.seek(0)
        data = json.load(f)
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info = '''%s 转账 %s 转账 %s 元''' % (new_time,turn_username, price)
        public_write(f, info, data)
    with open(DATA_PATH + 'bill.json', 'a+') as f:
        turn_info= '''%s %s 转入 %s 元''' % (new_time,username, price)
        month_time = time.strftime("%m", time.localtime())
        if turn_username not in data.keys():
            data[turn_username] = {}
            if month_time not in data[turn_username].keys():
                data[turn_username][month_time] = []
                data[turn_username][month_time].append(turn_info)
                write_log(f, data)
            else:
                data[turn_username][month_time].append(turn_info)
                write_log(f, data)
        else:
            if month_time not in data[turn_username].keys():
                data[turn_username][month_time] = []
                data[turn_username][month_time].append(turn_info)
                write_log(f, data)
            else:
                data[turn_username][month_time].append(turn_info)
                write_log(f, data)