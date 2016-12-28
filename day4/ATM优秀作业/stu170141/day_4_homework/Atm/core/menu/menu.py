# Author:houyafan
import os, sys,json
BASE_PASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PASH)
from core.data.CONST import BASE_PATH,DATA_PATH
from core.tools.check import *
from core.tools.public_file import *
from core.selectDeposit.selectDeposit import *
from core.modifyDeposit.modifyDeposit import *
from core.shopping.shopping import *
from core.returnDeposit.returnPrice import *
from core.takeDeposit.takeNow import *
from core.turnDeposit.turnPrice import *
from core.adminDeposit.admin import *
@public
def menu(): # menu_type 为入口标识  0是商场  1是Atm
    while True:
        menu_type_list=["商店","ATM","退出"]
        for index,item in enumerate(menu_type_list):
            print('\t\t\t', index, '\t\t\t', item)
        menu_type = input("请输入你要选择的功能编号:")
        if check_insert_number(menu_type,menu_type_list)[0]:
            tmp_num = check_insert_number(menu_type,menu_type_list)[1]
            if tmp_num == 0:
                shop_menu()
            elif tmp_num==1:
                flat_menu = True
                menu_list = ['还款', '查询', '转账', '提现', '管理', '退出']
                while flat_menu:
                    print('\t\t  \033[33;1m欢迎来到招商银行ATM机系统\033[0m')
                    for index, item in enumerate(menu_list):
                        print('\t\t\t', index, '\t\t\t', item)
                    function_menu = input("\033[33;1m请输入功能菜单:\033[0m")
                    if check_insert_number(function_menu, menu_list)[0]:
                        tmp = check_insert_number(function_menu, menu_list)[1]
                        if tmp == 0:  # 存款
                            returnPrice()
                        elif tmp == 1:  # 查询
                            select()
                        elif tmp == 2:  # 转账
                            turn_price()
                        elif tmp == 3:  # 体现
                            takeMoney()
                        elif tmp == 4:  # 管理
                            admin_user()
                        elif tmp == 5:  # 退出
                            break
            elif tmp_num==2:
                logout(DATA_PATH+'card_message_tmp.json')
                break
        else:
            pass
