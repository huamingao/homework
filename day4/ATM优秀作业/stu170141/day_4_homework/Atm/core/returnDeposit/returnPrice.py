# Author:houyafan
import os, sys, json,time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.modifyDeposit.modifyDeposit import *
from core.data.CONST import BASE_PATH, DATA_PATH
from core.tools.check import *
from core.tools.public_file import *

# 还款
@public
def returnPrice():
    returnMoney = input("请输入还款金额:")
    new_returnMoney = check_int(returnMoney)
    with open(DATA_PATH + "card_message_tmp.json", "r+")as f:
        data = json.load(f)
        username=get_username()
        creditmax = data[username]["message"]["CreditMax"]  # 信用卡剩余额度
        original = data[username]["message"]["Original"]  # 信用卡额度
        balance = data[username]["message"]["Balance"]  # 余额
        owed = original - creditmax  # 欠款
        if creditmax == original:  # 不欠款直接增加余额
            data[username]["message"]["Balance"] = balance+new_returnMoney
            write_file(f, data) # 写入返款
            write_return_bill(new_returnMoney) # 写入账单
        elif new_returnMoney == owed:  # 还款等于欠款
            data[username]["message"]["CreditMax"] = original
            write_file(f, data)
            write_return_bill(new_returnMoney)  # 写入账单
        elif new_returnMoney > owed:  # 还款大于欠款
            data[username]["message"]["CreditMax"] = original
            data[username]["message"]["Balance"] = balance + new_returnMoney - owed
            write_file(f, data)
            write_return_bill(new_returnMoney)  # 写入账单
        elif new_returnMoney < owed:  # 还款数小于欠款数
            if balance + new_returnMoney > owed:  # 余额+还款数>欠款
                data[username]["message"]["CreditMax"] = original
                data[username]["message"]["Balance"] = balance + new_returnMoney - owed
                write_file(f, data)
                write_return_bill(new_returnMoney)  # 写入账单
            elif balance + new_returnMoney < owed:  # 余额+还款数<欠款
                data[username]["message"]["Balance"] = 0
                data[username]["message"]["CreditMax"] = original - owed + balance + new_returnMoney
                write_file(f, data)
                write_return_bill(new_returnMoney)  # 写入账单
            elif balance + new_returnMoney == owed:  # 余额+还款数=欠款
                data[username]["message"]["Balance"] = 0
                data[username]["message"]["CreditMax"] = original
                write_file(f, data)
                write_return_bill(new_returnMoney)  # 写入账单
        elif balance == 0:  # 没有余额
            data[username]["message"]["CreditMax"] = new_returnMoney
            write_file(f, data)
            write_return_bill(new_returnMoney)  # 写入账单


# 写入账单
def write_return_bill(new_returnMoney):
    with open(DATA_PATH+'bill.json', 'a+') as f:
        f.seek(0)
        data=json.load(f)
        new_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info='''%s 还款 %s 元''' % (new_time,new_returnMoney)
        public_write(f, info, data)



