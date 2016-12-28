#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Author Xuyao

import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import bank
from bin import atm
from bin import mgmt

@atm.auth
def showList(_list):
    print("-------PRODUCTION INFO-------")
    print("ID    -NAME-         -PRICE-")
    for index, item in enumerate(_list):
        print("{_id}{_name}￥{_price}".format
              (_id=str(index + 1).ljust(6, ' '),
               _name=item[0].title().ljust(15, ' '),
               _price=str(item[1]).ljust(15, ' ')))
    print("-----------------------------")


def showCart(_list):
    if len(_list) != 0:
        print("-------CART LIST-------")
        print("NAME-         -PRICE-")
        for index, item in enumerate(_list):
            print("{_name}￥{_price}".format
                  (_name=item[0].title().ljust(15, ' '),
                   _price=str(item[1]).ljust(15, ' ')))
        print("-----------------------")


def loadData(_list, _filename):
    with open(_filename, 'r') as aFile:
        if os.path.getsize(_filename) != 0:
            for aItem in aFile.readlines():
                if aItem == '\n':
                    continue
                aItem = aItem.strip().split()
                _list.append(aItem)
            return True
        else:
            return False


def payment(_list,srcAccount,dstAccount):
    if len(_list) == 0:
        print("购物车为空，无需支付！")
        return False
    else:
        amount = 0.0
        for item in _list:
            amount += float(item[1])
        bank.transferAccounts(BASE_DIR+'/data/account.txt',srcAccount,dstAccount,amount)
        print(mgmt.colorStr("购买成功，欢迎继续购物！",32))
