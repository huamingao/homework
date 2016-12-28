#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Author Xuyao

import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import bank
from bin import mgmt


g_account = ''


def auth(_func):
    def decorate(*args, **kwargs):
        global g_account
        if g_account == '':
            print(mgmt.colorStr(">>>欢迎进入账户认证系统<<<", 36))
            count = 0
            while count < 3:
                card_num = input(mgmt.colorStr("请输入卡号:", 32))
                password = input(mgmt.colorStr("请输入密码:", 32))
                if bank.checkAuth(BASE_DIR + '/data/auth.txt', card_num, password):
                    print(mgmt.colorStr("认证通过！", 32))
                    g_account = card_num
                    break
                else:
                    if count < 2:
                        print(mgmt.colorStr("请再次尝试还有 %d 次机会！" % (2 - count), 31))
                count += 1
            else:
                print(mgmt.colorStr("认证失败！", 31))
                return False
        result = _func(*args, **kwargs)
        return result

    return decorate


@auth
def showMenu():
    menu_info = """>>>ATM系统<<<
1>  提现
2>  还款
3>  历史账单
4>  转账
5>  查询
6>  退出
"""
    print(mgmt.colorStr(menu_info, 36))


if __name__ == '__main__':
    while True:
        showMenu()
        choice = input("请输入命令编号进行相关操作：")
        choice_set = set(['1', '2', '3', '4', '5', '6'])
        if choice in choice_set:
            if choice == '1':
                amount = input("请输入提现金额：")
                bank.withdraw(BASE_DIR + '/data/account.txt', g_account, amount)
            elif choice == '2':
                amount = input("请输入还款金额：")
                bank.repayment(BASE_DIR + '/data/account.txt', g_account, amount)
            elif choice == '3':
                bank.showJournalByAccount(BASE_DIR + '/logs/journal.log', g_account)
            elif choice == '4':
                dst_account = input("请输入转入账户：")
                amount = input("请输入转账金额：")
                if bank.checkAccountExist(BASE_DIR + '/data/account.txt', dst_account):
                    bank.transferAccounts(BASE_DIR + '/data/account.txt', g_account, dst_account, amount)
            elif choice == '5':
                bank.showBalanceByAccount(BASE_DIR + '/data/account.txt',g_account)
            elif choice == '6':
                print(mgmt.colorStr("感谢您的使用！再见~", 32))
                exit()
            else:
                print(mgmt.colorStr("选择集合一定是被改动过了！", 31))
        else:
            print(mgmt.colorStr("无效的命令，请重新输入：", 31))
