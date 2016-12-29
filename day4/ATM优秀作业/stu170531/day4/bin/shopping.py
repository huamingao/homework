#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Author Xuyao

import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import shopping
from bin import atm

if __name__ == "__main__":
    goods_list = []
    newCart = []
    shopping_account = '0003'

    if shopping.loadData(goods_list, BASE_DIR + '/data/production.txt'):
        while True:
            shopping.showList(goods_list)
            choice = input("Id To Buy(num) / Pay(p):")

            if choice.isdigit():
                choice = int(choice)
                if choice <= len(goods_list) and choice > 0:
                    c_good = goods_list[choice - 1]
                    newCart.append(c_good)
                else:
                    print("The good you choosed is not exist!,try again!")
            elif choice == "p":
                shopping.showCart(newCart)
                shopping.payment(newCart, atm.g_account, shopping_account)
                exit()
            else:
                print("Invalid Option!")
    else:
        print("Vendor Is Running!")
