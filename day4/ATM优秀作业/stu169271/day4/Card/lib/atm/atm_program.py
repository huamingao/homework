#!/usr/bin/env python
# encoding: utf-8



import os
import datetime
import pickle
import logging

log_file = "../log/card_message.log"
lock_file = "../db/lock_account.txt"
user_info_file = "../db/user_info.pickle"
color_end = "\033[0m"
color_red = "\033[31;1m"
color_green = "\033[32;1m"
today = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
LOGIN_USER = {"is_login": False}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file,
                    filemode='w')

# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')


def file_is_exist(filename):
    if os.path.exists(filename):
        message = "True"
    else:
        message = "False"
    return message


def check_login(func):
    """
    装饰器函数：验证是否完成登录
    :param func: 要装饰的函数
    :return:
    """
    def inner(*args, **kwargs):
        # print(LOGIN_USER['is_login'])
        if LOGIN_USER['is_login']:
            r = func()
            return r
        else:
            print(color_red + "你还未登录，请登录" + color_end)
    return inner


def check_user_level(func):
    """
    装饰器函数：验证用户等级 0 普通用户 1 管理员
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        # print(LOGIN_USER['user_level'])
        # print(LOGIN_USER['user_level'] == "1")
        if LOGIN_USER['user_level'] == 1:
            r = func()
            return r
        else:
            print(color_red + "需要管理员权限" + color_end)
    return inner


def login(account_name, password):
    """
    验证用户登录
    :param account_name: 接受用户的登录账号
    :param password: 接受用户的登录密码
    :return:
    """
    res = file_is_exist(lock_file)   # 判断用户锁文件是否存在，不存在创建
    if res == "False":
        open(lock_file, "w+").close()

    count = 0
    flag = True
    while flag:
        if count < 3:                           # 只要重试不超过三次就不断循环
            with open(lock_file, 'r') as pas:   # 判断账号是否在锁定列表中，如果已经被锁定过，直接退出程序
                for line in pas.readlines():
                    if account_name in line:
                        print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
                        logging.info('%s 已经连续三次输出，账号被锁定' % account_name)
                        flag = False
                        break
            '''
              判断账号及密码是否在password.txt文件中存在且正确，如果正确记录日志，输出登录信息
            '''
            card_user_info_dict = pickle.load(open(user_info_file, 'rb'))
            user_name = card_user_info_dict[account_name].get('account_name')
            pass_word = card_user_info_dict[account_name].get('password')
            agree_flag = card_user_info_dict[account_name].get('agree_flag')
            account_stat = card_user_info_dict[account_name].get('account_stat')

            if account_name == user_name and password == pass_word and agree_flag == 1 and account_stat == 0:
                print(color_green + "欢迎 %s,登陆成功  !!!" % account_name + color_end)
                logging.info('%s 登陆成功' % account_name)
                LOGIN_USER['is_login'] = True
                LOGIN_USER['current_user'] = account_name
                LOGIN_USER['user_level'] = 0    # 设置用户等级 0 普通用户 1 管理员
                flag = False        			# 如果账号及密码信息正确，则记录日志，跳出循环
                break
            elif account_name == 'admin' and password == '123':
                print(color_green + "欢迎管理员登陆成功  !!!" + color_end)
                logging.info('%s 管理员登陆成功' % 'admin')
                LOGIN_USER['user_level'] = 1
                LOGIN_USER['is_login'] = True
                flag = False  # 如果账号及密码信息正确，则记录日志，跳出循环
                break
            else:
                print("账号密码错误或者账号未激活")
                count += 1
            # 如果同一个账号连续输错三次，则将账号记录到锁定文件列表，并退出程序
        else:
            print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
            logging.info('%s 已经连续三次输出，账号被锁定' % account_name)
            flag = False


def card_register_user():
    """
    信用卡申请功能
    :return:
    """
    res = file_is_exist(user_info_file)
    if res == "False":  # 判断文件是否存在，不存在则初始化文件,同时添加管理员信息
        card_user_info_dict = {}
        admin_info = {}
        admin_info["account_name"] = 'admin'
        admin_info["password"] = '123'
        admin_info["email"] = 'admin@qq.com'
        admin_info["phone_number"] = 12432423423
        admin_info["area_info"] = '北京'
        admin_info["agree_flag"] = 0            # 0 未审批 1 审批完成
        admin_info["agree_register"] = 0        # 0 审批失败 1 审批成功
        admin_info["card_limit"] = 0.0          # 用户信用额度，默认额度为0，审批通过然后进行额度授权 用户取现额度=用户信用额度余额/2
        admin_info["card_limit_surplus"] = 0.0  # 用户信用额度余额  用户取现额度余额=用户信用额度余额/2
        admin_info["account_stat"] = 0          # 0 账号正常使用 1 账号冻结
        admin_info["account_balance"] = 0.0     # 账户余额
        admin_info["bill_date"] = '25'          # 账单日期,默认每月25日
        admin_info["refund_date"] = '13'        # 还款日期，默认为每个月的13日
        card_user_info_dict['admin'] = admin_info

        pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))
    else:
        card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取原有的用户信息

    card_user_info = {}
    account_name = input("设置登录账号(审批通过生效)：")
    password = input("设置登录密码(审批通过生效)：")
    email = input("E-mail：")
    phone_number = input("手 机 号：")
    area_info = input("地区信息：")
    card_user_info["email"] = email
    card_user_info["phone_number"] = phone_number
    card_user_info["area_info"] = area_info
    card_user_info["agree_flag"] = 0                    # 0 未审批 1 审批完成
    card_user_info["agree_register"] = 0                # 0 审批失败 1 审批成功
    card_user_info["card_limit"] = 0.0                  # 用户信用额度，默认额度为0，审批通过然后进行额度授权
    card_user_info["card_limit_surplus"] = 0.0          # 用户信用额度余额
    card_user_info["account_name"] = account_name       # 信用卡登录账号 审批通过后生效
    card_user_info["password"] = password               # 信用卡登录密码 审批通过后生效
    card_user_info["account_stat"] = 0                  # 0 账号正常使用 1 账号冻结
    card_user_info["account_balance"] = 0.0             # 账号余额
    card_user_info["bill_date"] = '25'                  # 账单日期,默认每月25日
    card_user_info["refund_date"] = '13'                # 还款日期，默认为每个月的13日
    card_user_info_dict[account_name] = card_user_info

    pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))
    print(color_green + "信用卡申请信息已经提交，请耐心等待审批结果....." + color_end)
    logging.info('收到%s用户信用卡申请信息一条' % account_name)


def card_register_menu():
    """
    接收用户选择信用卡类型，引导用户完成申请
    :return:
    """
    while True:
        msg_03 = """
=========================================
            欢迎登陆xx信用卡中心
=========================================
        01、QQ会员联名信用卡
        02、火影忍者信用卡
        03、YOUNG卡（青年版）
        04、银联单币信用卡
        05、退出
=========================================
"""
        print(msg_03)
        choice_num = input("请选择信用卡类型：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            card_register_user()
        elif choice_num == 2:
            card_register_user()
        elif choice_num == 3:
            card_register_user()
        elif choice_num == 4:
            card_register_user()
        else:
            break


def audit_user_register():
    """
    审核用户的信用卡申请信息，授权额度
    :return:
    """
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取原有的用户信息
    print("已经有的申请信息(审批状态：0 未审批 1 审批完成 )：")
    for i in card_user_info_dict.keys():
        user_info_msg = """
账号：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%.2f\t\t取现额度：%.2f\t\t账号余额：%2.f
        """ % (card_user_info_dict[i].get('account_name'),
               card_user_info_dict[i].get('phone_number'),
               card_user_info_dict[i].get('email'),
               card_user_info_dict[i].get('area_info'),
               card_user_info_dict[i].get('agree_flag'),
               card_user_info_dict[i].get('card_limit'),
               card_user_info_dict[i].get('card_limit')/2,
               card_user_info_dict[i].get('account_balance'),)
        print(user_info_msg.strip("\n"))
    while True:
        card_user_agree = input("请选择账号进行审批(q 退出)：")
        if card_user_agree == "q" or card_user_agree == "quit":
            break
        else:
            for i in card_user_info_dict.keys():
                if card_user_agree == card_user_info_dict[i]['account_name']:
                    user_info_msg = """
账号：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%.2f\t\t取现额度：%.2f\t\t账号余额：%2.f
                            """ % (card_user_info_dict[i].get('account_name'),
                                   card_user_info_dict[i].get('phone_number'),
                                   card_user_info_dict[i].get('email'),
                                   card_user_info_dict[i].get('area_info'),
                                   card_user_info_dict[i].get('agree_flag'),
                                   card_user_info_dict[i].get('card_limit'),
                                   card_user_info_dict[i].get('card_limit') / 2,
                                   card_user_info_dict[i].get('account_balance'),)
                    print(user_info_msg.strip("\n"))

        card_agree = input("是否同意该用户申请(y/n):")
        if card_agree == "yes" or card_agree == "y":
            card_user_info_dict[card_user_agree]['agree_flag'] = 1
        else:
            break

        card_agree_limit = input("请输入授权额度：")
        if card_agree_limit.strip().isdigit():
            card_agree_limit = float(card_agree_limit)
        card_user_info_dict[card_user_agree]['card_limit'] = card_agree_limit
        card_user_info_dict[card_user_agree]['card_limit_surplus'] = card_agree_limit
        pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件
        logging.info('审批用户申请信息一条，审批结果%s，授权额度%2.f元' % (
            card_user_info_dict[i].get('agree_flag'),
            card_user_info_dict[i].get('card_limit')))
        for i in card_user_info_dict.keys():
            user_info_msg = """
账号：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%.2f\t\t取现额度：%.2f\t\t账号余额：%2.f
            """ % (card_user_info_dict[i].get('account_name'),
                   card_user_info_dict[i].get('phone_number'),
                   card_user_info_dict[i].get('email'),
                   card_user_info_dict[i].get('area_info'),
                   card_user_info_dict[i].get('agree_flag'),
                   card_user_info_dict[i].get('card_limit'),
                   card_user_info_dict[i].get('card_limit') / 2,
                   card_user_info_dict[i].get('account_balance'),)
            print(user_info_msg.strip("\n"))


def card_limit_manager():
    """
    管理用户额度功能
    :return:
    """
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))
    for i in card_user_info_dict.keys():
        user_info_msg = """
账号：%s\t\t手机号:%s\t\t邮箱：%s\t\t地区：%s\t\t审批状态：%s\t\t用户额度：%.2f\t\t取现额度：%.2f\t\t账号余额：%2.f
        """ % (card_user_info_dict[i].get('account_name'),
               card_user_info_dict[i].get('phone_number'),
               card_user_info_dict[i].get('email'),
               card_user_info_dict[i].get('area_info'),
               card_user_info_dict[i].get('agree_flag'),
               card_user_info_dict[i].get('card_limit'),
               card_user_info_dict[i].get('card_limit') / 2,
               card_user_info_dict[i].get('account_balance'),)
        print(user_info_msg.strip("\n"))
    while True:
        card_limit_user = input("请输入要调整额度的账号：")  # 要完善退出功能
        if card_limit_user in card_user_info_dict.keys():
            card_limit_sum = input("请输入要调整的额度：")
            if card_limit_sum.strip().isdigit():
                card_limit_sum = float(card_limit_sum)
            card_user_info_dict[card_limit_user]['card_limit'] = \
                int(card_user_info_dict[card_limit_user]['card_limit']) + card_limit_sum
            card_user_info_dict[card_limit_user]['card_limit_surplus'] = card_user_info_dict[card_limit_user]['card_limit']
            pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件
            break
        else:
            print("账号输入错误，请重新输入")
            continue


def frozen_account_manager():
    """
    冻结账号
    :return:
    """
    account_name = input("请输入要冻结的账号：")
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取原有的用户信息
    card_user_info_dict[account_name]['account_stat'] = 1
    pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))
    print(color_green + "该用账号已经被冻结....." + color_end)


@check_login
@check_user_level
def atm_user_manager_menu():
    while True:
        msg_01 = """
=========================================
            欢迎登陆xx信用卡中心
=========================================
    01、审批用户申请(审批并授权用户额度)
    02、用户额度管理
    03、冻结账号
    04、退出
=========================================
"""
        print(msg_01)
        choice_num = input("请选择：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            audit_user_register()
        elif choice_num == 2:
            card_limit_manager()
        elif choice_num == 3:
            frozen_account_manager()
        else:
            break


@check_login
def credit_card_limit():
    """
    用户个人额度查询及申请调整额度
    :return:
    """
    while True:
        msg_02 = """
=========================================
            欢迎登陆xx信用卡中心
=========================================
        01、额度查询
        02、申请调临额
        03、申请调固额
        04、退出
=========================================
    """
        print(msg_02)
        choice_num = input("请选择：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
            for i in card_user_info_dict.keys():
                user_info_msg = """
=========================================
        姓名：%s
        手机号:%s
        邮箱：%s
        地区：%s
        审批状态：%s
        账单日期：每月%s日
        还款日期：每月%s日
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余额度：%.2f
        取现剩余额度：%.2f
=========================================
                """ % (card_user_info_dict[i].get('account_name'),
                       card_user_info_dict[i].get('phone_number'),
                       card_user_info_dict[i].get('email'),
                       card_user_info_dict[i].get('area_info'),
                       card_user_info_dict[i].get('agree_flag'),
                       card_user_info_dict[i].get('bill_date'),
                       card_user_info_dict[i].get('refund_date'),
                       card_user_info_dict[i].get('account_balance'),
                       card_user_info_dict[i].get('card_limit'),
                       card_user_info_dict[i].get('card_limit') / 2,
                       card_user_info_dict[i].get('card_limit_surplus'),
                       card_user_info_dict[i].get('card_limit_surplus') / 2,)
                if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
                    print(user_info_msg.strip("\n"))
        elif choice_num == 2:
            card_limit_change = input("请输入要临时调整的额度金额：")
            if card_limit_change.strip().isdigit():
                card_limit_change = int(card_limit_change)
            print(color_green + "额度调整申请信息已经提交，请耐心等待审批结果....." + color_end)
        elif choice_num == 3:
            card_limit_change = input("请输入要固定调整的额度金额：")
            if card_limit_change.strip().isdigit():
                card_limit_change = int(card_limit_change)
            print(color_green + "额度调整申请信息已经提交，请耐心等待审批结果....." + color_end)
        else:
            break


@check_login
def card_get_cash():
    """
    提现功能
    :return:
    """
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
    current_user = ""
    for i in card_user_info_dict.keys():
        if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
            user_info_msg = """
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
=========================================
                            """ % (card_user_info_dict[i].get('account_balance'),
                                   card_user_info_dict[i].get('card_limit'),
                                   card_user_info_dict[i].get('card_limit') / 2,
                                   card_user_info_dict[i].get('card_limit_surplus'),
                                   card_user_info_dict[i].get('card_limit_surplus') / 2,)
            print(user_info_msg.strip("\n"))
            current_user = card_user_info_dict[i]['account_name']
    while True:
        card_cash_sum = input("请输入要取现的金额(q退出)：")
        if card_cash_sum == "q" or card_cash_sum == "quit":
            break
        else:
            if card_cash_sum.strip().isdigit():
                card_cash_sum = int(card_cash_sum)
            if card_user_info_dict[current_user]["card_limit_surplus"]/2 >= card_cash_sum + card_cash_sum * 0.05:
                a = card_cash_sum * 0.05
                print("取现成功（收取%%5的手续费）手续费小计：%.2f元" % a)
                card_user_info_dict[current_user]["card_limit_surplus"] = \
                    card_user_info_dict[current_user]["card_limit_surplus"] - card_cash_sum*2 - a*2
                pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件
            else:
                print(color_red + "额度不足，请检查！！！" + color_end)
                continue
    for i in card_user_info_dict.keys():
        if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
            user_info_msg = """
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
=========================================
            """ % (card_user_info_dict[i].get('account_balance'),
                   card_user_info_dict[i].get('card_limit'),
                   card_user_info_dict[i].get('card_limit') / 2,
                   card_user_info_dict[i].get('card_limit_surplus'),
                   card_user_info_dict[i].get('card_limit_surplus') / 2,)
            print(user_info_msg.strip("\n"))

@check_login
def card_transfer_accounts():
    """
    信用卡转账功能
    :return:
    """
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
    current_user = ""
    for i in card_user_info_dict.keys():
        if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
            user_info_msg = """
=========================================
        欢迎%s, 登录xxx信用卡中心
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
=========================================
            """ % (LOGIN_USER['current_user'],
                   card_user_info_dict[i].get('account_balance'),
                   card_user_info_dict[i].get('card_limit'),
                   card_user_info_dict[i].get('card_limit') / 2,
                   card_user_info_dict[i].get('card_limit_surplus'),
                   card_user_info_dict[i].get('card_limit_surplus') / 2,)
            print(user_info_msg.strip("\n"))
            current_user = card_user_info_dict[i]['account_name']

    transfer_to_user = input("请输入要转账的账号：")
    if transfer_to_user in card_user_info_dict.keys():
        transfer_to_sum = input("请输入转账的金额：")
        transfer_to_sum = float(transfer_to_sum)
        card_user_info_dict[current_user]["card_limit_surplus"] = \
            card_user_info_dict[current_user]["card_limit_surplus"] - transfer_to_sum*2
        card_user_info_dict[transfer_to_user]["account_balance"] = \
            card_user_info_dict[transfer_to_user]["account_balance"] + transfer_to_sum
        pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
    current_user = ""
    for i in card_user_info_dict.keys():
        if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
            user_info_msg = """
=========================================
        欢迎%s, 登录xxx信用卡中心
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
=========================================
                        """ % (LOGIN_USER['current_user'],
                               card_user_info_dict[i].get('account_balance'),
                               card_user_info_dict[i].get('card_limit'),
                               card_user_info_dict[i].get('card_limit') / 2,
                               card_user_info_dict[i].get('card_limit_surplus'),
                               card_user_info_dict[i].get('card_limit_surplus') / 2,)
            print(user_info_msg.strip("\n"))

@check_login
def credit_card_payment():
    """
    信用卡还款功能
    :return:
    """
    card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
    current_user = ""
    for i in card_user_info_dict.keys():
        if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
            user_info_msg = """
=========================================
        欢迎%s, 登录xxx信用卡中心
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
        待还款金额：%2.f
=========================================
注：待还款金额=用户额度-剩余用户额度-账号余额
=========================================
                """ % (LOGIN_USER['current_user'],
                       card_user_info_dict[i].get('account_balance'),
                       card_user_info_dict[i].get('card_limit'),
                       card_user_info_dict[i].get('card_limit') / 2,
                       card_user_info_dict[i].get('card_limit_surplus'),
                       card_user_info_dict[i].get('card_limit_surplus') / 2,
                       card_user_info_dict[i].get('card_limit') -
                       card_user_info_dict[i].get('account_balance') -
                       card_user_info_dict[i].get('card_limit_surplus'),)
            print(user_info_msg.strip("\n"))
            current_user = card_user_info_dict[i]['account_name']
    while True:
        credit_card_payment_flag = input("是否还款（y/n）：")
        if credit_card_payment_flag == 'y' or credit_card_payment_flag == "yes":
            credit_card_payment_sum = input("请输入还款总额：")
            credit_card_payment_sum = float(credit_card_payment_sum)
            card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
            card_user_info_dict[current_user]["card_limit_surplus"] = \
                card_user_info_dict[current_user]["card_limit_surplus"] + \
                (credit_card_payment_sum - card_user_info_dict[current_user].get('account_balance'))
            pickle.dump(card_user_info_dict, open(user_info_file, 'wb'))  # 将审批完成的信息写会文件
        else:
            card_user_info_dict = pickle.load(open(user_info_file, 'rb'))  # 获取用户信息
            current_user = ""
            for i in card_user_info_dict.keys():
                if LOGIN_USER['current_user'] == card_user_info_dict[i]['account_name']:
                    user_info_msg = """
=========================================
        欢迎%s, 登录xxx信用卡中心
=========================================
        账户余额：%2.f
        用户额度：%.2f
        取现额度：%.2f
        剩余用户额度：%.2f
        剩余取现额度：%.2f
        待还款金额：%2.f
=========================================
注：待还款金额=用户额度-剩余用户额度-账号余额
=========================================
                            """ % (LOGIN_USER['current_user'],
                                   card_user_info_dict[i].get('account_balance'),
                                   card_user_info_dict[i].get('card_limit'),
                                   card_user_info_dict[i].get('card_limit') / 2,
                                   card_user_info_dict[i].get('card_limit_surplus'),
                                   card_user_info_dict[i].get('card_limit_surplus') / 2,
                                   card_user_info_dict[i].get('card_limit') -
                                   card_user_info_dict[i].get('account_balance') -
                                   card_user_info_dict[i].get('card_limit_surplus'),)
                    print(user_info_msg.strip("\n"))
            break


def atm_main():
    while True:
        msg_01 = """
=========================================
            欢迎登陆xx信用卡中心
=========================================
        01、申请信用卡
        02、账号登录
        03、额度管理
        04、提现
        05、账单查询（未出账单、已出账单）
        06、转账
        07、还款
        08、ATM用户管理（管理员权限）
        09、退出
=========================================
    """
        print(msg_01)
        choice_num = input("请选择：")
        if choice_num.strip().isdigit():
            choice_num = int(choice_num)
        if choice_num == 1:
            card_register_menu()
        elif choice_num == 2:
            account_name = input("账号：")
            password = input("密码：")
            login(account_name, password)
        elif choice_num == 3:
            credit_card_limit()
        elif choice_num == 4:
            card_get_cash()
        elif choice_num == 5:
            pass
        elif choice_num == 6:
            card_transfer_accounts()
        elif choice_num == 7:
            credit_card_payment()
        elif choice_num == 8:
            atm_user_manager_menu()
        else:
            exit('欢迎下次光临')

#
# if __name__ == '__main__':
#     main()
