import json,time,os,sys
base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
from core import atm,public,shoppingmall
def menu():
    '''程序入口，可选择atm和商城入口'''
    print("\033[1;36m----欢迎来到商家购物平台！----\n\033[1;32m[0]ATM系统\n[1]购物中心\033[0m：")
    choice = input("\033[1;33m温馨提示：输出q可退出本程序！\033[1;36m\n请选择您的操作:\033[0m")
    if choice == '0':
        print("\033[1;33m您选择了\033[1;32m[ATM操作系统]\033[0m")
        atm.atm_list()
    elif choice == '1':
        print("\033[1;33m您选择了\033[1;32m[商家购物中心]\033[0m")
        shoppingmall.shopping_mall()
    elif choice == 'q':
        print("\033[1;31m正在退出程序...欢迎下次光临，再见！\033[0m")
        exit()
    else:
        print("\033[1;31m选择错误，请重新选择！\033[0m")
        menu()
menu()