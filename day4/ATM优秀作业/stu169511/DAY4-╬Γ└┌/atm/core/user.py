import os,json,sys,time
base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from core import atm,public
from db import *
from core.auth import *
user_json = base_dir + os.path.sep + 'db' + os.path.sep + 'user.json'
bill_json = base_dir + os.path.sep + 'db' + os.path.sep + 'bill.json'
def user():
    user_choice = input("\033[1;36m请选择您的操作：\033[0m")
    if user_choice == '0':
        print("\033[1;32m您选择了[0]额度查询操作！\033[0m")
        cced()
    elif user_choice == '1':
        print("\033[1;32m您选择了[1]账单查询操作！\033[0m")
        billing()
    elif user_choice == '2':
        print("\033[1;32m您选择了[2]转账操作！\033[0m")
        transfer()
    elif user_choice == '3':
        print("\033[1;32m您选择了[3]还款操作！\033[0m")
        repay()
    elif user_choice == 'b':
        print("\033[1;32m您选择了回到管理界面！\033[0m")
        return user()
    elif user_choice == 'q':
        print("\033[1;31m欢迎下次光临，再见！\033[0m")
        exit()
    else:
        print("\033[1;31m输入错误，请重新输入！\033[0m")
        return user()
def cced():
    '''查询余额和信息'''
    cced_user = input("\033[1;36m请输入您要查询的账户姓名：\033[0m")#获取用户名
    cced_list = public.op_file(user_json)#获取所有用户信息
    try:
        cced_info = cced_list[cced_user]  # 获取当前用户账户信息
        if cced_info in cced_list:
            user_info_credit = cced_info['credit']#用户额度
            user_balance = cced_info['balance']#用户余额
            print("\033[1;32m用户%s的额度是：%s,余额是：%s\033[0m" % (cced_user,user_info_credit,user_balance))
            user()
    except KeyError:
        print("\033[1;31m您要查询的账户不存在，请重新输入！")
        cced()
def billing():
    '''查询账单'''
    bill_user = input("\033[1;36m请输入您要查询的账户姓名：\033[0m")
    bill_month = input("\033[1;36m请输入您要查询的月份：\033[0m")
    bill_list = public.op_file(bill_json)#获取所有用户的账单信息
    try:
        bill_info = bill_list[bill_user]  # 获取当前用户的账单信息
        if bill_month.isdigit():
            bill_month = int(bill_month)
            if 1 <= bill_month <= 12:
                if bill_user in bill_list and bill_month in bill_info:
                    for bill in bill_info[bill_month]:
                        print("\033[1;32m您%s月份的账单信息是：\033[1;33m%s\033[0m"%(bill_month,bill))
                        user()
                else:
                    bill_choice = input("\033[1;31m本月无账单！是否继续操作？y or q?\033[0m")
                    if bill_choice == 'y':
                        print("\033[1;32m您选择了继续操作\033[0m")
                        billing()
                    elif bill_choice == 'q':
                        print("\033[1;31m欢迎下次光临，再见！\033[0m")
                        exit()
                    else:
                        print("\033[1;31m输入错误，回到大厅。。。\033[0m")
                        user()
            else:
                print("\033[1;31m查询月份输入错误，请重新输入！\033[0m")
                billing()
        else:
            print("\033[1;31m查询月份输入错误，请重新输入！\033[0m")
            billing()
    except KeyError:
        print("\033[1;31m您要查询的账户不存在，请重新输入！")
        billing()
def transfer():
    '''转账'''
def repay():
    '''还款'''
    repay_user = input("\033[1;36m请输入您要还款的账户姓名：\033[0m")#获取用户名
    repay_list = public.op_file(user_json)  # 获取所有用户信息
    try:
        repay_info = repay_list[repay_user]  # 获取当前用户账户信息
        if repay_user in repay_list:
            # user_credit = repay_info['credit']  # 用户信用额度
            # user_base_credit = repay_info['base_credit']#用户基础额度
            repay_money = repay_info['base_credit'] - repay_info['credit']#欠款
            user_balance = repay_info['balance']  # 用户余额
            money = input("\033[1;36m请输入您的还款金额：\033[0m")
            if money.isdigit():
                money = int(money)
                if money > 0:
                    if repay_money == 0:#若不欠款，还款加入余额
                        repay_info['balance'] += money
                    elif money >= repay_money:#若还款大于等于欠款，恢复信用额度，余额等于余额+还款-欠款
                        repay_info['credit'] = repay_info['base_credit']
                        repay_info['balance'] += money-repay_money
                    elif money < repay_money and repay_money <= money + user_balance:
                    #若欠款大于还款，且欠款小于等于还款+余额；恢复信用额度，余额等于余额+还款-欠款
                        repay_info['credit'] = repay_info['base_credit']
                        repay_info['balance'] += money - repay_money
                    elif money < repay_money and user_balance == 0:
                        repay_info['credit'] += money
                    elif repay_money > money + user_balance:
                        repay_info['credit'] += money + user_balance
                        repay_info['balance'] = 0
                    f = open(user_json, 'w')
                    f.write(json.dumps(repay_list))
                    f.close()
                    print("\033[1;32m还款成功，还款%s元，账户额度%s元，余额%s元"%(money,repay_info['credit'],repay_info['balance']))
                    public.write_atm_log('%s %s 还款 %s元'%(repay_user,time.strftime("%Y-%m-%d %H:%M:%S"),money))#还款信息写入日志
                else:
                    print("\033[1;31m金额不能输入为0！\033[0m")
                    repay()
            else:
                print("\033[1;31m金额输入错误！请输入正确的数字！\033[0m")
                repay()
    except KeyError:
        print("\033[1;31m用户名不存在！请重新输入！\033[0m")
        repay()