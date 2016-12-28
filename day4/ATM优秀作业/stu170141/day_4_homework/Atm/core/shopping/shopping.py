# Author:houyafan
import json, os, sys,datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.data.CONST import BASE_PATH, DATA_PATH
from core.menu.menu import *
from core.tools.public_file import *
from core.modifyDeposit.modifyDeposit import *
salary_list = []

@public
def shop_menu():
    while True:
        with open(DATA_PATH+'produck.json', 'r') as f:
            produck_data = json.load(f)
        for i in produck_data.items():
            print(i)
        change_menu = input("请输入要选择的商品(退出请输入q)：")
        if change_menu in produck_data:
            salary = produck_data[change_menu]
            modify(salary)
        elif change_menu == "q":
            break
        else:
            print("请输入正确的商品名称")
            continue
