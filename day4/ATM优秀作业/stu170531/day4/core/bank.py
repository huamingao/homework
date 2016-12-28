#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Author Xuyao

import sys, os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from bin import mgmt


def checkFreeze(_func):
    def decorate(*args, **kwargs):
        with open(args[0], 'r') as account_file:
            for line in account_file:
                line = line.strip().split()
                if line[0] == args[1]:
                    if line[-1] == '1':
                        print(mgmt.colorStr("账户 %s 已被冻结！" % line[0], 31))
                        return False
        result = _func(*args, **kwargs)
        return result

    return decorate


def writeJournal(_func):
    def decorate(*args, **kwargs):
        result = _func(*args, **kwargs)
        with open(BASE_DIR + '/logs/mgmt.log', 'a', encoding='utf-8') as journal:
            timestamp = time.strftime('%Y-%m-%d(%H:%M:%S)', time.localtime(time.time()))
            if len(args) > 2:
                journal_str = timestamp + ' ' + str(args[1]) + ' '+_func.__name__+'>>'+str(args[2])+ '\n'
            else:
                journal_str = timestamp + ' ' + str(args[1]) + ' ' + _func.__name__ + '\n'
            journal.write(journal_str)
        return result

    return decorate

@writeJournal
def addAccount(filename, *args):
    with open(filename, 'r', encoding='utf-8') as account_file:
        for line in account_file:
            if line.split()[0] == args[0]:
                print(mgmt.colorStr("账户已经存在！",31))
                return False
    with open(filename, 'a', encoding='utf-8') as account_file:
        record = ' '.join(args)
        account_file.write(record + '\n')
        return True

def addAuth(filename, *args):
    with open(filename, 'r', encoding='utf-8') as account_file:
        for line in account_file:
            if line.split()[0] == args[0]:
                print(mgmt.colorStr("账户已经存在！",31))
                return False
    with open(filename, 'a', encoding='utf-8') as account_file:
        record = ' '.join(args)
        account_file.write(record + '\n')
        return True

@writeJournal
def delAccount(filename, account):
    pass


def checkFreezeStatus(filename, account):
    if checkAccountExist(filename, account):
        with open(filename, 'r', encoding='utf-8') as account_file:
            for line in account_file:
                if line.split()[0] == account:
                    line = line.strip().split()
                    if line[4] == '1':
                        return True
                    elif line[4] == '0':
                        return False
                    else:
                        exit("数据错误！")

@writeJournal
def freeze(filename, account):
    if checkAccountExist(filename, account):
        with open(filename, 'r', encoding='utf-8') as account_file:
            with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
                for line in account_file:
                    if line.split()[0] == account:
                        line = line.strip().split()
                        line[4] = '1'
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
        print(mgmt.colorStr("账户%s已经冻结！" % str(account), 32))
        os.remove(filename)
        os.rename(filename + '_tmp', filename)

@writeJournal
def unFreeze(filename, account):
    if checkAccountExist(filename, account):
        with open(filename, 'r', encoding='utf-8') as account_file:
            with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
                for line in account_file:
                    if line.split()[0] == account:
                        line = line.strip().split()
                        line[4] = '0'
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
        print(mgmt.colorStr("账户%s已经解冻！" % str(account), 32))
        os.remove(filename)
        os.rename(filename + '_tmp', filename)

@writeJournal
def setLimit(filename, account, limit):
    if checkAccountExist(filename, account):
        with open(filename, 'r', encoding='utf-8') as account_file:
            with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
                for line in account_file:
                    if line.split()[0] == account:
                        line = line.strip().split()
                        line[2] = str(limit)
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
        print(mgmt.colorStr("账户%s当前的最高信用额度为%s." % (account, limit), 32))
        os.remove(filename)
        os.rename(filename + '_tmp', filename)


@checkFreeze
def transferAccounts(filename, srcAccount, dstAccount, amount):
    with open(filename, 'r', encoding='utf-8') as account_file:
        with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
            cca = checkCreditAmount(filename, srcAccount, float(amount))
            if type(cca) != bool and float(amount) > 0:
                for line in account_file:
                    if line.split()[0] == srcAccount:
                        line = line.strip().split()
                        line[3] = str(float(line[3]) - float(amount))
                        line = " ".join(line) + '\n'
                    elif line.split()[0] == dstAccount:
                        line = line.strip().split()
                        line[3] = str(float(line[3]) + float(amount))
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
            elif float(amount) <= 0:
                print(mgmt.colorStr("无效的转账金额！", 31))
                return False
    os.remove(filename)
    os.rename(filename + '_tmp', filename)
    addJournal(BASE_DIR + '/logs/journal.log', srcAccount, -float(amount), "transferOut>>%s" % str(dstAccount))
    addJournal(BASE_DIR + '/logs/journal.log', dstAccount, float(amount), "transferIn<<%s" % str(srcAccount))
    print("转账成功，转账金额为:%s" % str(amount))
    print("您当前的剩余信用额度为： %s" % str(cca))
    return True


def showAccounts(filename):
    with open(filename, 'r', encoding='utf-8') as account_file:
        output = " %-8s %-15s %-9s %-7s %-6s"
        print("\033[0;32;0mCARD-NO.    NAME          LIMIT    BALANCE  FREEZE\033[0m")
        for line in account_file:
            line = line.strip().split()
            print(output % (line[0], line[1], line[2], line[3], line[4]))


@checkFreeze
def checkAuth(filename, account, passwd):
    with open(filename, 'r', encoding='utf-8') as auth_file:
        for line in auth_file:
            line = line.strip().split()
            if account == line[0] and passwd == line[1]:
                return True
        else:
            return False


def checkCreditAmount(filename, account, amount):
    with open(filename, 'r', encoding='utf-8') as account_file:
        for line in account_file:
            if line.split()[0] == account:
                line = line.strip().split()
                cur_credit = float(line[2]) + float(line[3]) - float(amount)
                if cur_credit > 0:
                    return cur_credit
                else:
                    print(mgmt.colorStr("您的剩余信用额度不足，请还款或控制消费金额！", 31))
                    return False


@checkFreeze
def withdraw(filename, account, amount):
    print(mgmt.colorStr("信用卡提现将额外收取%5的手续费，公安机关提醒：坚决打击套现、洗钱等违法行为！", 35))
    print("正在提现，请稍候...")
    time.sleep(1)
    with open(filename, 'r', encoding='utf-8') as account_file:
        with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
            if float(amount) < 0:
                print(mgmt.colorStr("无效的金额！ %s" % amount, 31))
            fee = float(amount) * 1.05
            cca = checkCreditAmount(filename, account, fee)
            if type(cca) != bool:
                for line in account_file:
                    if line.split()[0] == account:
                        line = line.strip().split()
                        line[3] = str(float(line[3]) - fee)
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
            else:
                return False
    os.remove(filename)
    os.rename(filename + '_tmp', filename)
    addJournal(BASE_DIR + '/logs/journal.log', account, -fee, "withdraw")
    print("提现成功，提现金额为:%s" % str(amount))
    print("您当前的剩余信用额度为： %s" % str(cca))
    return True


@checkFreeze
def repayment(filename, account, amount):
    print(mgmt.colorStr("公安机关提醒：坚决打击套现、洗钱等违法行为！", 35))
    print("正在还款，请稍候...")
    time.sleep(1)
    with open(filename, 'r', encoding='utf-8') as account_file:
        with open(filename + '_tmp', 'w', encoding='utf-8') as tmp_file:
            if float(amount) < 0:
                print(mgmt.colorStr("无效的金额！ %s" % amount, 31))
            cca = checkCreditAmount(filename, account, (-float(amount)))
            if type(cca) != bool:
                for line in account_file:
                    if line.split()[0] == account:
                        line = line.strip().split()
                        line[3] = str(float(line[3]) + float(amount))
                        debt = float(line[3])
                        line = " ".join(line) + '\n'
                    tmp_file.write(line)
            else:
                return False
    os.remove(filename)
    os.rename(filename + '_tmp', filename)
    addJournal(BASE_DIR + '/logs/journal.log', account, amount, "repayment")
    print("还款成功，还款金额为:%s" % str(amount))
    if debt < 0:
        print("仍需还款: %s " % str(abs(debt)))
    else:
        print("账户余额: %s" % str(debt))
    return True


def checkAccountExist(filename, account):
    with open(filename, 'r', encoding='utf-8') as account_file:
        for line in account_file:
            line = line.strip().split()
            if line[0] == account:
                return True
        else:
            print(mgmt.colorStr("账户不存在！", 31))
            return False


def addJournal(filename, account, amount, type):
    with open(filename, 'a', encoding='utf-8') as journal:
        timestamp = time.strftime('%Y-%m-%d(%H:%M:%S)', time.localtime(time.time()))
        journal_str = timestamp + ' ' + str(account) + ' ' + str(amount) + ' ' + str(type) + '\n'
        journal.write(journal_str)


def showJournalByAccount(filename, account):
    with open(filename, 'r', encoding='utf-8') as journal:
        for line in journal:
            line = line.strip().split()
            if line[1] == str(account):
                print("账号%s 于%s 进行了 %s 操作，流动金额 %s " % (line[1], line[0], line[3], line[2]))


def showAllJournal(filename):
    with open(filename, 'r', encoding='utf-8') as journal:
        for line in journal:
            line = line.strip().split()
            print("账号%s 于%s 进行了 %s 操作，流动金额 %s " % (line[1], line[0], line[3], line[2]))


def showManipulate(filename):
    with open(filename, 'r', encoding='utf-8') as journal:
        for line in journal:
            line = line.strip().split()
            print("%s 对账号%s 进行了 %s 操作" % (line[0], line[1], line[2]))


def showBalanceByAccount(filename, account):
    with open(filename, 'r', encoding='utf-8') as account_file:
        for line in account_file:
            line = line.strip().split()
            if line[0] == str(account):
                print("""您的余额为：%s\n您的最高信用额度为:%s
您的剩余信用额度为: %s\n""" % (line[3], line[2], str(float(line[3]) + float(line[2]))))
                return True
        else:
            return False



