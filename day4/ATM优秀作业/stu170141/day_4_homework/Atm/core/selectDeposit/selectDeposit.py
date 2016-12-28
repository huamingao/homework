# Author:houyafan
import os, sys, json
from core.data.CONST import BASE_PATH, DATA_PATH

from core.tools.check import *
from core.tools.public_file import *
from core.modifyDeposit.modifyDeposit import *


# 查询方法
@public
def select():
    username = get_username()
    menu_list = ['查询总信用额度', '查询消费账单', '查询剩余额度', '退出']
    while True:
        print('\t\t  \033[33;1m欢迎来到招商银行ATM机系统\033[0m')
        for index, item in enumerate(menu_list):
            print('\t\t\t', index, '\t\t\t', item)
        function_menu = input("\033[33;1m请输入功能菜单:\033[0m")
        if check_insert_number(function_menu, menu_list)[0]:
            tmp = check_insert_number(function_menu, menu_list)[1]
            if tmp == 0:  # 查询信用额度 和 余额
                with open(DATA_PATH + 'card_message_tmp.json', 'r', encoding='utf-8')as f:
                    data = json.load(f)
                print("你的信用卡总额度为\033[32;1m%s\033[0m元." % data[username]["message"]["Original"])
            elif tmp == 1:
                with open(DATA_PATH + 'bill.json', 'r')as f:
                    data = json.load(f)
                    if username in data.keys():
                        data_num = input('请输入要查询的月份(1-12):')
                        if data_num in data[username].keys():
                            for item in data[username][data_num]:
                                print(item)
                        else:
                            print("\033[32;1m您输入的月份暂无费用记录...\033[0m")
                    else:
                        print("\033[32;1m您暂时没有费用记录...\033[0m")
            elif tmp == 2:
                with open(DATA_PATH + 'card_message_tmp.json', 'r+') as f:
                    data = json.load(f)
                    print("您的信用额度剩余\033[32;1m%s\033[0m元,余额剩余\033[32;1m%s\033[0m元" % (
                    data[username]["message"]["CreditMax"], data[username]["message"]["Balance"]))
            elif tmp == 3:
                break
        elif not check_insert_number(function_menu, menu_list)[0]:
            continue
