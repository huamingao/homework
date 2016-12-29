import os,sys
base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from db import *
from core import public,manager,user
USER_JSON = base_dir + os.path.sep + 'db' + os.path.sep + 'user.json'
from core.auth import *
@auth
def atm_list():
    print("\033[1;36m----欢迎来到ATM操作系统！----\n\033[1;32m请输入用户名密码进入到相对应的管理界面！\033[0m")
    dic = public.op_file(USER_JSON)
    user_name = input("\033[1;36m请输入您的用户名\033[0m")
    pass_word = input("\033[1;36m请输入您的密码\033[0m")
    if user_name in dic:
        if dic[user_name]['type'] == 'manager'and dic[user_name]['passwd'] == pass_word:
            print("\033[1;36m欢迎回到管理员操作平台，您具有以下操作权限：\n\033[1;32m[0]冻结账户\n[1]额度调整\n[2]添加账户\n[3]解锁用户\n[4]注销\033[0m")
            manager.manager()
        elif dic[user_name]['type'] == 'user' and dic[user_name]['passwd'] == pass_word:
            print("\033[1;36m欢迎回到用户管理平台，您具有以下操作权限：\n\033[1;32m[0]额度查询\n[1]账单查询\n[2]转账\n[3]还款\033[0m")
            user.user()
        else:
            print("\033[1;31m用户名或密码错误，请重新输入！\033[0m")
            atm_list()
    else:
        print("\033[1;31m用户名不存在！请重新输入！\033[0m")
        atm_list()