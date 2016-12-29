#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Author Xuyao

import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import bank
from bin import mgmt


def colorStr(aStr, color_code):
    return "\033[0;" + str(color_code) + ";0m" + aStr + "\033[0m"


admin_account = ''


def authCheck(_func):
    def decorate(*args, **kwargs):
        global admin_account
        if admin_account == '':
            print(mgmt.colorStr(">>>欢迎进入账户认证系统<<<", 36))
            count = 0
            while count < 3:
                card_num = input(mgmt.colorStr("请输入管理员账号:", 32))
                admin_account = card_num
                password = input(mgmt.colorStr("请输入密码:", 32))
                if card_num == 'admin' and password == '123':
                    print(mgmt.colorStr("认证通过！", 32))
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


@authCheck
def showMenu():
    menu_info = """>>>银行后台管理系统<<<
1>  查看账户
2>  冻结/解冻账户
3>  更改额度
4>  增加账户
5>  查看流水
6>  操作日志
7>  退出
"""
    print(mgmt.colorStr(menu_info, 36))


if __name__ == '__main__':
    while True:
        showMenu()
        choice = input("请输入命令编号进行相关操作：")
        choice_set = set(['1', '2', '3', '4', '5', '6', '7'])
        if choice in choice_set:
            if choice == '1':
                bank.showAccounts(BASE_DIR + '/data/account.txt')
            elif choice == '2':
                account = input(mgmt.colorStr("请输入要变更的账户：", 32))
                if bank.checkFreezeStatus(BASE_DIR + '/data/account.txt', account):
                    bank.unFreeze(BASE_DIR + '/data/account.txt', account)
                else:
                    bank.freeze(BASE_DIR + '/data/account.txt', account)
            elif choice == '3':
                account = input(mgmt.colorStr("请输入要变更的账户：", 32))
                limit = input(mgmt.colorStr("请输入要设定的额度：", 32))
                bank.setLimit(BASE_DIR + '/data/account.txt', account, limit)
            elif choice == '4':
                account = input(mgmt.colorStr("请输入要添加的新账户名：", 32))
                username = input(mgmt.colorStr("请输入新用户名：", 32))
                password = input(mgmt.colorStr("请输入新密码：", 32))
                account_list = [account, username, '15000', '0.0', '0']
                auth_list = [account, password]
                bank.addAccount(BASE_DIR + '/data/account.txt', *account_list)
                bank.addAuth(BASE_DIR + '/data/auth.txt', *auth_list)
            elif choice == '5':
                bank.showAllJournal(BASE_DIR + '/logs/journal.log')
            elif choice == '6':
                bank.showManipulate(BASE_DIR + '/logs/mgmt.log')
            elif choice == '7':
                print(mgmt.colorStr("退出后台管理系统...", 32))
                exit()
            else:
                print(mgmt.colorStr("选择集合一定是被改动过了！", 31))
        else:
            print(mgmt.colorStr("无效的命令，请重新输入：", 31))
