#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import json
import time
import datetime
import logging

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DB = os.path.join(PROJECT_DIR,'db')

from src import crontab as src_crontab
from src import admin as src_admin
from src import client as src_client
from lib import validator


CURRENT_USER_INFO = {'is_authenticated':False,'username':''}

# main函数（普通用户入口）中用到的交互文字
MAIN_MENU = """
欢迎来到用户自助服务平台
1、登录账户
2、查看账户
3、购买商品
4、查看账单
5、我要提现
6、我要还款
7、我要转账
退出并注销，请输q
"""
LOGOFF_MSG = '{username} 您已成功退出并注销'
OPTION_PROMPT = '请输入您的选项：'
INVALID_MSG = '您的输入不合法，请重新输入！'
EXIT_MSG = '\033[31;1m您已成功退出当前画面\033[0m'
INPUT_TO_CONTINUE = '\033[31;1m若要继续操作，请输任意键\033[0m'


# login函数中用到的交互文字
LOGIN_MSG = '\033[31;1m您尚未登录！请按下面提示登录，若要中途退出，请输q：\033[0m'
INPUT_USERNAME = '普通用户登录，请输入信用卡卡号：'
INPUT_PASSWORD = '请输入登录密码：'
SUCCESS_LOGIN = '\033[31;1m{username}，您已成功登陆信用卡自助服务系统！\033[0m'
AUTO_JUMP_BACK = '系统为您自动跳转到上一个画面...请按提示继续操作'
NO_EXIST_USER = '\033[31;1m您输入的用户名不存在！请重新输入！\033[0m'
PWD_INVALID = '\033[31;1m密码错误，请重新输入用户名/信用卡号和密码！\033[0m'
ADMIN_AUTO_JUMP = '{username}，您输入的是管理员用户名，为您自动跳转到后台管理界面'

# print_user函数中用到的交互文字
CARD_INFO = """
信用卡号：{card_num}
持卡人姓名：{username}
刷卡密码：{password}
信用卡额度：{credit}
当前可用额度：{balance}
当前储蓄金额：{savings}
卡片状态：{status}
账单日：每月1日
还款日：每月{enroll_date}日
过期时间：{expire_date}
欠款记录："""
NO_DEBT = '没有欠款记录'
CURRENT_CARD_MSG = '您的信用卡账户信息如下：'
NO_EXIST_CARD = '\033[31;1m您输入的卡号不存在！\033[0m'
INPUT_CARD_NUM = '请输入要查询的信用卡卡号,若要中途退出，请输q：'
DEBT_MENU = '账单月份  欠款总额  账单状态  滞纳金'

# shopping函数中用到的文字
LOCKED_MSG = '您的账户已被冻结，无法进行交易，请联系管理员！'
WEL_MSG = '欢迎来到购物商城！'.center(50, '*')
MENU_MSG = '编号 商品 价格'
RULE_MSG = '''规则：退出商城，请输q；返回上层，请输b；查看消费记录，请输c；
*****************************************************'''
LIST_MSG = '若要进入子类目，请输入对应的编号！\n'
CURRENT_CATEGORY_MSG = '您已来到类目：'
FAIL_BACK_MSG = '\033[31;1m已经达到顶层，无法返回上层！\033[0m'
PURCHASE_MSG = '您已成功购入以下商品:'
MONEY_MSG = '当前可用额度：'
NOMONEY_MSG = '\033[31;1m额度不足\033[0m'
QUANTITY_PROMPT = '请输入您要购买的商品数量：'
ACHEIVE_EMBED_MSG = '您已到达商品价格列表！若要购买，请输入相应的商品编号！'
REC_SHOPPING = 'successfully pay for {quantity} quantity {product},total cost {cost} RMB'

# withdraw_credit函数中用到的文字
INPUT_WITHDRAW = '请输入要提现的金额：'
NO_ENOUGH_BALANCE = '账户可用额度不足，无法完成提现！'
REC_WITHDRAW = 'successfully withdraw {money}RMB, from savings {savings}RMB, from credit {withdraw_credit}RMB, withdraw fee is {fee}RMB'
WITHDRAW_CREDIT = '您已成功提现{money}RMB，其中从储蓄金免费提现{savings}RMB，从信用额度提现{withdraw_credit}RMB，提现费用为{fee}RMB'

# show_bill函数中用到的文字
INPUT_MONTH_SHOW = '查询账单，请输入年月，输入格式如201610；若要中途退出，请输q：'
VERIFY_REPAY = '确认要全额还款？确认请输非q的任意键；放弃还款，请输q：'
NO_BILL = '该月份没有账单记录'

# make_out_bill函数中用到的文字
REC_MAKE_OUT_BILL = 'has made out the bill for this month: debt {debt} in {month}'

# calculate_delay_fee
REC_DELAY_FEE = 'The latest delay fee for the debt in {month} is {delay_fee}, the latest total debt for {month} is {debt} '

# repay_debt
MONTH_DEBT = '{month}，待还款总额为{month_debt}'
RESTORE_CREDIT = '实时为您恢复额度，当前可用额度为：{balance}'
INPUT_MONTH_REPAY = '账单还款，请输入月份，输入格式如201609；若要中途退出，请输q：'
REC_REPAY_DEBT = 'successfully repay {debt}RMB for {month}'

# transfer用到的函数
INPUT_TRANSFER_CARD_NUM= '转账，请输入要转入资金的卡号：'
INPUT_MONEY = '请输入要转入的金额：'
NO_ENOUGH_SAVINGS = '您的储蓄金额不够，请先提现足够多的钱到储蓄池，再进行转账'
REC_TRANSFER_TO = 'you have transfered {money}RMB out to card_num {card_num}'
REC_TRANSFER_IN = 'card_num {card_num} has transfered {money}RMB to you'
SUCCESS_TRANSFER = '您已成功向卡号{card_num}转账{money}RMB'
SAME_CARD = '您输入的转入卡号与当前登录卡号相同，无法进行转账'



def outer(func):
    """
    装饰器，在执行任何其他函数之前先执行login函数
    :param func:
    :return:
    """
    def inner(*args,**kwargs):
        if not CURRENT_USER_INFO['is_authenticated']:
            login()
        return func(*args,**kwargs)
    return inner


def login():
    """
    普通用户登录
    :return:
    """
    if CURRENT_USER_INFO['is_authenticated']:
        print(SUCCESS_LOGIN.format(username=CURRENT_USER_INFO['username']))
        print(AUTO_JUMP_BACK)
        return True
    else:
        print(LOGIN_MSG)
        while True:
            card_num = input(INPUT_USERNAME)
            if card_num == 'q':
                print(EXIT_MSG,AUTO_JUMP_BACK)
                main()
            if card_num not in os.listdir(PROJECT_DB):
                print(NO_EXIST_USER)
            else:
                # 调用load_current_user,从userinfo文件读取信息，赋值给全局变量CURRENT_USER_INFO
                load_current_user(card_num)
                if CURRENT_USER_INFO['user_type'] == 'admin':
                    print(ADMIN_AUTO_JUMP.format(username=CURRENT_USER_INFO['username']))
                    src_admin.main()
                else:
                    password = input(INPUT_PASSWORD)
                    if password == 'q':
                        print(EXIT_MSG, AUTO_JUMP_BACK)
                        main()
                    if password != CURRENT_USER_INFO['password']:
                        print(PWD_INVALID)
                    else:
                        CURRENT_USER_INFO['is_authenticated'] = True
                        # 调用函数自动在每月1日出账单，并计算欠款滞纳金
                        make_out_bill()
                        print(SUCCESS_LOGIN.format(username = CURRENT_USER_INFO['username']))
                        print(AUTO_JUMP_BACK)
                        return None




def load_current_user(card_num):
    """
    从文件读取信用卡用户信息，赋值给全局变量CURRENT_USER_INFO
    :param card_num:
    :return:
    """
    userinfo_file = os.path.join(PROJECT_DB, card_num, 'userinfo')
    userinfo_dict = json.load(open(userinfo_file, 'r'))
    CURRENT_USER_INFO.update(userinfo_dict)


def dump_current_user(current_user_info):
    """
    把全局变量current_user_info dump到对应用户的userinfo文件中
    :param current_user_info:
    :return:
    """
    user_info = current_user_info.copy()
    del user_info['is_authenticated']
    userinfo_file = os.path.join(PROJECT_DB, user_info['card_num'], 'userinfo')
    json.dump(current_user_info, open(userinfo_file, 'w'))


def print_user(card_num=None):
    while True:
        if not card_num:
            card_num = input(INPUT_CARD_NUM)
        if card_num == 'q':
            return 'q'
        user_dir = os.path.join(PROJECT_DB,card_num)
        if not os.path.exists(user_dir):
            print(NO_EXIST_CARD)
        else:
            load_current_user(card_num)
            print(CURRENT_CARD_MSG)
            print(CARD_INFO.format(card_num = CURRENT_USER_INFO['card_num'],
                                   username = CURRENT_USER_INFO['username'],
                                   password = CURRENT_USER_INFO['password'],
                                   credit = CURRENT_USER_INFO['credit'],
                                   balance = CURRENT_USER_INFO['balance'],
                                   savings = CURRENT_USER_INFO['savings'],
                                   enroll_date = time.localtime(CURRENT_USER_INFO['enroll_date']).tm_mday,
                                   expire_date = datetime.date.fromtimestamp(CURRENT_USER_INFO['expire_date']),
                                   status = CURRENT_USER_INFO['status']
                                   ))
            if not CURRENT_USER_INFO['debt']:
                print(NO_DEBT)
                return card_num
            else:
                print(DEBT_MENU)
                for debt in CURRENT_USER_INFO['debt']:
                    print(debt['month'],debt['month_debt'],debt['status'],debt['delay_fee'],sep=' ')
                return card_num


def calculate_debt_balance(debt):
    """
    每当发生欠款，调用此函数更新全局变量CURRENT_USER_INFO['debt']
    如果发生欠款的当月，此前已存在欠款记录，CURRENT_USER_INFO['debt']['month']自增
    如果发生欠款的当月，尚无欠款记录，CURRENT_USER_INFO['debt']新增一条记录
    :param cost:
    :return:
    """
    # 获取当前月份
    month = str(time.localtime().tm_year) + str(time.localtime().tm_mon)
    # # 如果欠款记录为空，新增一条当前月份的欠款记录
    # if not CURRENT_USER_INFO['debt']:
    #     CURRENT_USER_INFO['debt'].append({'month': month, 'month_debt': debt,'status':'unbill','delay_fee':0})
    # # 如果欠款记录不为空
    # else:
    flag = 0
    # 遍历欠款记录，如果已经有当前月份的欠款记录，追加当月的month_debt
    for month_debt in CURRENT_USER_INFO['debt']:
        if month == month_debt['month']:
            flag = 1
            month_debt['month_debt'] += debt
    # 如果没有遍历到当前月份的欠款记录，新增一条当前月份的欠款记录
    if not flag:
        CURRENT_USER_INFO['debt'].append({'month': month, 'month_debt': debt,'status':'pending billing','delay_fee':0})
    dump_current_user(CURRENT_USER_INFO)


@outer
def shopping():
    """
    购物商城
    :return:
    """
    print(WEL_MSG)
    # 获得商品列表
    goods_file = os.path.join(PROJECT_DB,'goods')
    current_goods_list = goods_list = json.load(open(goods_file,'r'))
    option = ''
    while option != 'q':
        print(MENU_MSG)
        for i, product in enumerate(current_goods_list):
            #如果到达位于最底层的商品价格列表，打印编号、商品、价格
            if type(current_goods_list[product]) == int:
                print(i + 1, product, current_goods_list[product])
            # 否则，只打印编号、商品类目
            else:
                print(i + 1, product)
        print(RULE_MSG)
        # 提示用户输入选项
        option = input(OPTION_PROMPT)
        if option == 'q':
            return 'q'
        # 如果输入c,调用show_bill函数，打印欠款清单
        elif option == 'c':
            show_bill()
            option = input(INPUT_TO_CONTINUE)
        # 如果输入b，且当前菜单不是顶层菜单，则返回上级菜单
        elif option == 'b':
            if current_goods_list != goods_list:
                for item in goods_list.values():
                    if item == current_goods_list:
                        current_goods_list = goods_list
                for subdic in goods_list.values():
                    for item in subdic.values():
                        if item == current_goods_list:
                            current_goods_list = subdic
            # 如果输入b时正处于商城最顶层，退出商城
            else:
                return 'q'
        # 如果输入的option存在于当前菜单编号列表中
        elif option.isdigit() and int(option) in range(len(current_goods_list.keys())+1):
            # 如果当前菜单的下一级就是商品价格列表（最底层的价格是整型，基于此做判断）
            if type(current_goods_list[product]) == int :
                if CURRENT_USER_INFO['status'] == 1:
                    print(LOCKED_MSG)
                    return None
                elif CURRENT_USER_INFO['status'] == 0:
                    print(ACHEIVE_EMBED_MSG)
                    # 获得输入编号对应的商品名
                    keys = current_goods_list.keys()
                    index = int(option) - 1
                    product = list(keys)[index]
                    # 提示输入要购买的商品数量，调用input_isdigit函数强制必须输入数字
                    quantity = int(validator.force_digit(QUANTITY_PROMPT, INVALID_MSG))
                    cost = current_goods_list[product] * quantity
                    # 如果总价大于余额，提示余额不够
                    if cost > CURRENT_USER_INFO['balance']:
                        print(MONEY_MSG,CURRENT_USER_INFO['balance'],NOMONEY_MSG)
                        option = input(INPUT_TO_CONTINUE)
                    # 否则余额充足，余额减去总价得到新的余额，取出本次购买信息，包括产品、数量，打印购买成功
                    else:
                        CURRENT_USER_INFO['balance'] -= cost
                        calculate_debt_balance(cost)
                        print(PURCHASE_MSG, quantity, product,'\n',MONEY_MSG,CURRENT_USER_INFO['balance'])
                        log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record',time.strftime("%Y%m"))
                        write_record(CURRENT_USER_INFO,log_file,
                                     REC_SHOPPING.format(product=product,quantity=quantity,cost=cost))
                        option = input(INPUT_TO_CONTINUE)
            # 如果下一级菜单不是商品价格列表，即仍为商品类目
            else:
                # 根据当前菜单，打印'已来到XX类目'
                for i,item in enumerate(current_goods_list.keys()):
                    if i == int(option) - 1:
                        menu = item
                        print(CURRENT_CATEGORY_MSG,menu,LIST_MSG)
                        break
                # 将当前菜单置为下一级菜单，进入下轮循环
                values_list = list(current_goods_list.values())
                # 根据编号option 获取对应类目/商品所在的索引位置
                index = int(option) - 1
                current_goods_list = values_list[index]
        else:
            # 如果用户输入不满足以上条件，打印输入不合法，并提示是否继续购物，获得重新输入的option
            print(INVALID_MSG)
            option = input(INPUT_TO_CONTINUE)


def write_record(user_dict,log_file,message):
    """
    账户记录
    :param message:
    :return:
    """
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(message)


@outer
def withdraw_credit():
    """
    提现，可用信用balance额度减少，储蓄savings增加
    :return:
    """
    money = float(validator.force_digit(INPUT_WITHDRAW,INVALID_MSG))
    # 如果储蓄金savings足够，就从savings中取钱
    if CURRENT_USER_INFO['savings'] >= money:
        savings = money
        CURRENT_USER_INFO['savings'] -= money
        fee = 0
    else:
        savings = CURRENT_USER_INFO['savings']
        # 要从信用卡额度提现的金额，即需要计算提现手续费的那部分提现金额
        withdraw_credit = money - savings
        fee = withdraw_credit * 0.05
        # 如果要提现的钱大于储蓄金savings，继续第二步判断当前可用信用额度是否足够用来提现
        if withdraw_credit + fee > CURRENT_USER_INFO['balance']:
            print(NO_ENOUGH_BALANCE)
       # 如果要提现的钱大于储蓄金savings，取出全部savings，剩余部分从当前可用信用额度提取
        else:
            CURRENT_USER_INFO['savings'] = 0
            debt = withdraw_credit + fee
            CURRENT_USER_INFO['balance'] -= debt
            dump_current_user(CURRENT_USER_INFO)
            calculate_debt_balance(debt)
    log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record',time.strftime("%Y%m"))
    write_record(CURRENT_USER_INFO,log_file,REC_WITHDRAW.format(money=money,
                    savings=savings,withdraw_credit=withdraw_credit,fee=fee))
    print(WITHDRAW_CREDIT.format(money=money,savings=savings,withdraw_credit=withdraw_credit,fee=fee))



@outer
def repay_debt():
    if not CURRENT_USER_INFO['debt']:
        print(NO_DEBT)
    else:
        while True:
            # 遍历欠款记录
            for month_debt in CURRENT_USER_INFO['debt']:
                # 只打印已经出账的账单
                if month_debt['status'] == 'already billed':
                    print(MONTH_DEBT.format(month=month_debt['month'],month_debt=month_debt['month_debt']))
            month = str(validator.force_digit(INPUT_MONTH_REPAY,INVALID_MSG))
            if month == 'q':
                return 'q'
            # 遍历欠款记录，如果输入的月份存在于欠款记录中
            for month_debt in CURRENT_USER_INFO['debt']:
                flag = 0
                if month == month_debt['month']:
                    flag = 1
                    # 确认要全额还款？输q表示放弃还款
                    if input(VERIFY_REPAY) == 'q':
                        return 'q'
                    else:
                        # 更新CURRENT_USER_INFO中的可用余额
                        temp = CURRENT_USER_INFO['balance'] + month_debt['month_debt']
                        CURRENT_USER_INFO['balance'] = min(CURRENT_USER_INFO['credit'],temp)
                        # 移除debt记录
                        CURRENT_USER_INFO['debt'].remove(month_debt)
                        dump_current_user(CURRENT_USER_INFO)
                        print(RESTORE_CREDIT.format(balance=CURRENT_USER_INFO['balance']))
                        log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record',time.strftime("%Y%m"))
                        write_record(CURRENT_USER_INFO,log_file,REC_REPAY_DEBT.format(debt=month_debt['month_debt'],month=month_debt['month']))
                        return None
            if not flag:
                print(NO_BILL)



@outer
def show_bill():
    """
    查看账单，输入要查询的月份，打印该月份账单流水
    :return:
    """
    while True:
        month = str(validator.force_digit(INPUT_MONTH_SHOW, INVALID_MSG))
        if month == 'q':
            return 'q'
        bill_file = os.path.join(PROJECT_DB,CURRENT_USER_INFO['card_num'],'record',month)
        if not os.path.exists(bill_file):
            print(NO_BILL)
        else:
            with open(bill_file,'r') as f:
                for line in f:
                    print(line,end='')
            return None

def make_out_bill():
    """
    每月1日是账单日，出上月账单，出账后CURRENT_USER_INFO['debt']['status']从pending billing置为already billed
    每月enroll_date为还款日，若逾期未还，按以下标准收取滞纳金：*0.01*滞纳天数*欠款
    :return:
    """
    # 获取当前日期和月份
    today_date = time.localtime().tm_mday
    last_month = str(time.localtime().tm_mon - 1)
    if int(last_month) < 10:
        last_month = str(time.localtime().tm_year) + '0' + last_month
    else:
        last_month = str(time.localtime().tm_year) + last_month
    # 如果1日是账单日，CURRENT_USER_INFO['debt']['status']置为already billed
    if today_date == 1:
        month_debt = 0
        # 遍历得到上月欠款总额
        for debt in CURRENT_USER_INFO['debt']:
            if debt['month'] == last_month:
                month_debt = debt['month_debt']
                debt['status'] = 'already billed'
                dump_current_user(CURRENT_USER_INFO)
                # 写一条出账记录到日志文件
                log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record', last_month)
                write_record(CURRENT_USER_INFO,log_file,REC_MAKE_OUT_BILL.format(debt=month_debt, month=last_month))
                break
    # 计算还款日(即发卡日)
    enroll_date = datetime.datetime.fromtimestamp(CURRENT_USER_INFO['enroll_date']).day
    # 如果当前日期已过还款日，计算要计滞纳金的天数
    if today_date >= enroll_date:
        days = today_date - enroll_date
    else:
        days = (enroll_date - today_date) + 30
    # 遍历欠款记录
    for debt in CURRENT_USER_INFO['debt']:
        # 对于有欠款记录的月份，即status是already billed
        if debt['status'] == 'already billed':
            # 计算该月欠款的滞纳天数
            year_diff = time.localtime().tm_year - int(debt['month'][:4])
            month_diff = time.localtime().tm_mon - (int(debt['month'][4:6]) + 1)
            if month_diff < 0:
                month_diff = time.localtime().tm_mon + (12 - ((int(debt['month'][4:6]))+1))
            day_diff = today_date - enroll_date
            if day_diff < 0:
                day_diff = today_date + (30 - enroll_date)
            days = year_diff * 365 + month_diff * 30 + day_diff
            # 复利计算滞纳金和欠款
            n = 1
            while n <= days:
                # 每过一天，滞纳金都会增加
                debt['delay_fee'] += 0.01 * debt['month_debt']
                # 每过一天，欠款都会增加滞纳金
                debt['month_debt'] += 0.01 * debt['month_debt']
                # 将更新写入到当前用户的userinfo文件
                dump_current_user(CURRENT_USER_INFO)
                n += 1
            # 写一条滞纳金记录到日志文件
            log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record', debt['month'])
            write_record(CURRENT_USER_INFO, log_file, REC_DELAY_FEE.format(delay_fee=debt['delay_fee'],
                                                                           debt=debt['month_debt'],
                                                                           month=debt['month']))



@outer
def transfer():
    """
    转账，只能从储蓄金额savings中转账倒别的卡的savings
    :return:
    """
    card_num = input(INPUT_TRANSFER_CARD_NUM)
    if card_num not in os.listdir(PROJECT_DB):
        print(NO_EXIST_CARD)
    elif card_num == CURRENT_USER_INFO['card_num']:
        print(SAME_CARD)
    else:
        money = validator.force_digit(INPUT_MONEY,INVALID_MSG)
        if CURRENT_USER_INFO['savings'] < money:
            print(NO_ENOUGH_SAVINGS)
        else:
            # 打印转账成功
            print(SUCCESS_TRANSFER.format(card_num=card_num,money=money))
            # 更新转出卡的userinfo文件
            CURRENT_USER_INFO['savings'] -= money
            dump_current_user(CURRENT_USER_INFO)
            log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record', time.strftime("%Y%m"))
            write_record(CURRENT_USER_INFO,log_file,REC_TRANSFER_TO.format(money=money,card_num=card_num))
            # 更新转入卡的userinfo文件
            partner_file = os.path.join(PROJECT_DB,card_num,'userinfo')
            partner_dict = json.load(open(partner_file,'r'))
            partner_dict['savings'] += money
            log_file = os.path.join(PROJECT_DB, CURRENT_USER_INFO['card_num'], 'record', time.strftime("%Y%m"))
            write_record(partner_dict,log_file,REC_TRANSFER_IN.format(money=money,card_num=card_num))
            json.dump(partner_dict, open(partner_file, 'w'))



def main():
    ret = True
    while True:
        if ret == 'q':
            print(EXIT_MSG,AUTO_JUMP_BACK)
        elif not ret:
            input(INPUT_TO_CONTINUE)
        print(MAIN_MENU)
        option = input(OPTION_PROMPT)
        if option == 'q':
            print(LOGOFF_MSG.format(username = CURRENT_USER_INFO['username']))
            CURRENT_USER_INFO.clear()
            CURRENT_USER_INFO['is_authenticated'] = False
            src_crontab.main()
        if option == '1':
            ret = login()
        elif option == '2':
            if not CURRENT_USER_INFO['is_authenticated']:
                ret = login()
            if CURRENT_USER_INFO['is_authenticated']:
                card_num = CURRENT_USER_INFO['card_num']
                ret = print_user(card_num)
                if ret != 'q':
                    ret = None
        elif option == '3':
            ret = shopping()
        elif option == '4':
            ret = show_bill()
        elif option == '5':
            ret = withdraw_credit()
        elif option == '6':
            ret = repay_debt()
        elif option == '7':
            ret = transfer()
        else:
            print(INVALID_MSG)
            ret = False



