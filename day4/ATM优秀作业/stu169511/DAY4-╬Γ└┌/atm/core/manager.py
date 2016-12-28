import os,json,sys
base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from core import atm,public
from db import *
USER_JSON = base_dir + os.path.sep + 'db' + os.path.sep + 'user.json'
def manager():
    manager_choice = input("\033[1;36m请选择您的操作：\033[0m")
    if manager_choice == '0':
        print("\033[1;32m您选择了[0]账号冻结操作！\033[0m")
        freeze_card()
    elif manager_choice == '1':
        print("\033[1;32m您选择了[1]调整额度操作！\033[0m")
        update_card()
    elif manager_choice == '2':
        print("\033[1;32m您选择了[2]新增账户操作！\033[0m")
        insert_card()
    elif manager_choice == '3':
        print("\033[1;32m您选择了[3]解锁账户操作！\033[0m")
        deblocking()
    elif manager_choice == 'b':
        print("\033[1;32m您选择了回到管理界面！\033[0m")
        return manager()
    elif manager_choice == 'q':
        print("\033[1;31m欢迎下次光临，再见！\033[0m")
        exit()
    else:
        print("\033[1;31m输入错误，请重新输入！\033[0m")
        return manager()
def freeze_card():
    freeze_card_user = input("\033[1;36m请输入您要冻结的账户姓名：\033[0m")
    free_card_list = public.op_file(USER_JSON)
    try:
        freeze_info = free_card_list[freeze_card_user]
        user_info_status = freeze_info['status']
        if freeze_card_user in free_card_list and user_info_status == 0:
            free_card_new = freeze_info.update({'status': 1})
            dic_new = free_card_list.update({freeze_card_user: freeze_info})
            f = open(USER_JSON, 'w')
            f.write(json.dumps(free_card_list))
            f.close()
            print("\033[1;32m冻结操作成功，该用户已被冻结且无法登录！\033[0m")
            return freeze_card()
        elif freeze_card_user in free_card_list and user_info_status == 1:
            print("\033[1;31m账户已被锁定，无需重复操作！\033[0m")
            reply_choice = input("\033[1;32m请问您是否继续操作？y确定操作，q退出程序\033[0m")
            if reply_choice == 'y':
                print("\033[1;32m您选择了继续操作\033[0m")
                return freeze_card()
            elif reply_choice == 'q':
                print("\033[1;31m欢迎下次光临，再见！\033[0m")
                exit()
            else:
                print("\033[1;31m输入错误，回到大厅。。。\033[0m")
                atm.atm_list()
    except KeyError:
        print("\033[1;31m用户名不存在！\033[0m")
        reply_choice = input("\033[1;32m请问您是否继续操作？y确定操作，q退出程序\033[0m")
        if reply_choice == 'y':
            print("\033[1;32m您选择了继续操作\033[0m")
            return freeze_card()
        elif reply_choice == 'q':
            print("\033[1;31m欢迎下次光临，再见！\033[0m")
            exit()
        else:
            print("\033[1;31m输入错误，回到大厅。。。\033[0m")
            atm.atm_list()
def update_card():
    update_card_info = input("\033[1;36m请输入您要调整的账户姓名：\033[0m")
    update_info = public.op_file(USER_JSON)#获取所有账户信息
    try:
        if update_card_info in update_info:
            new_credit = input("\033[1;36m请输入您增加的额度：\033[0m")
            if new_credit.isdigit():
                new_credit = int(new_credit)
                if new_credit % 100 ==0:
                    update_info[update_card_info]['base_credit'] += new_credit
                    update_info[update_card_info]['credit'] += new_credit
                    update_credit = update_info[update_card_info].update({'credit':update_info[update_card_info]['credit']})
                    update_base_credit =update_info[update_card_info].update({'base_credit':update_info[update_card_info]['base_credit']})
                    dic_new = update_info.update({update_card_info: update_info[update_card_info]})
                    f = open(USER_JSON, 'w')
                    f.write(json.dumps(update_info))
                    print("\033[1;31m用户名%s添加成功！\033[0m" % update_card_info)
                    next_step = input("\033[1;34m请问您是否要继续操作？继续请输入y，退出请输入q!\033[0m")
                    if next_step == 'y':
                        return update_card()
                    elif next_step == 'q':
                        print("\033[1;31m欢迎下次光临，再见！\033[0m")
                        exit()
                    else:
                        print("\033[1;31m输入错误，回到上级页面。。。\033[0m")
                        return update_card()
            else:
                print("\033[1;31m请输入正整数，且为100的倍数！\033[0m")
                return update_card()
    except KeyError:
        print("\033[1;31m用户名不存在！\033[0m")
        reply_choice = input("\033[1;32m请问您是否继续操作？y确定操作，q退出程序\033[0m")
        if reply_choice == 'y':
            print("\033[1;32m您选择了继续操作\033[0m")
            return update_card()
        elif reply_choice == 'q':
            print("\033[1;31m欢迎下次光临，再见！\033[0m")
            exit()
        else:
            print("\033[1;31m输入错误，回到大厅。。。\033[0m")
            atm.atm_list()
def insert_card():
    insert_user = input('\033[1;36m请输入您要添加的账户名：\033[0m')
    insert_user_list = public.op_file(USER_JSON)
    if len(insert_user)>0:
        if insert_user in insert_user_list:
            print("\033[1;31m用户名已存在！\033[0m")
            return insert_card()
        else:
            dic = {
                insert_user: {"passwd": "123123", "status": 0, "type": "user", "credit": 15200,
                               "base_credit": 15200,
                               "balance": 0
                }
            }
            dic_new = insert_user_list.update(dic)
            f = open(USER_JSON, 'w')
            f.write(json.dumps(insert_user_list))
            f.flush()
            print("\033[1;31m用户名%s添加成功！\033[0m" % insert_user)
            next_step = input("\033[1;34m请问您是否要继续操作？继续请输入y，退出请输入q!\033[0m")
            if next_step == 'y':
                return insert_card()
            elif next_step == 'q':
                print("\033[1;31m欢迎下次光临，再见！\033[0m")
                exit()
            else:
                print("\033[1;31m输入错误，回到上级页面。。。\033[0m")
                return insert_card()
    else:
        print("\033[1;31m输入错误，请重新操作！\033[0m")
        return insert_card()
def deblocking():
    deblocking_card_user = input("\033[1;36m请输入您要解锁的账户姓名：\033[0m")
    deblocking_card_list = public.op_file(USER_JSON)
    try:
        deblocking_info = deblocking_card_list[deblocking_card_user]
        user_info_status = deblocking_info['status']
        if deblocking_card_user in deblocking_card_list and user_info_status == 1:
            deblocking_card_new = deblocking_info.update({'status': 0})
            dic_new = deblocking_card_list.update({deblocking_card_user: deblocking_info})
            f = open(USER_JSON, 'w')
            f.write(json.dumps(deblocking_card_list))
            f.close()
            print("\033[1;32m解冻成功，该账户可正常登录！\033[0m")
            return deblocking()
        elif deblocking_card_user in deblocking_card_list and user_info_status == 0:
            print("\033[1;31m账户为解锁状态，无需重复解锁\033[0m")
            return deblocking()
    except KeyError:
        print("\033[1;31m用户名不存在！\033[0m")
        reply_choice = input("\033[1;32m请问您是否继续操作？y确定操作，q退出程序\033[0m")
        if reply_choice == 'y':
            print("\033[1;32m您选择了继续操作\033[0m")
            return deblocking()
        elif reply_choice == 'q':
            print("\033[1;31m欢迎下次光临，再见！\033[0m")
            exit()
        else:
            print("\033[1;31m输入错误，回到大厅。。。\033[0m")
            atm.atm_list()