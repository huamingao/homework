#!/usr/bin/env python
# encoding: utf-8



import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.atm.atm_program import *
from src.shopping_mall.shopping_mall_pg import *


def main():
    msg_main = """
======================================
            1、信用卡中心
            2、购物商场
            3、退出
======================================
    """
    while True:
        print(msg_main)
        choice_num = input("请选择：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            atm_main()
        elif choice_num == 2:
            shopping_mall_main()
        else:
            exit("欢迎下次光临")


if __name__ == '__main__':
    main()
