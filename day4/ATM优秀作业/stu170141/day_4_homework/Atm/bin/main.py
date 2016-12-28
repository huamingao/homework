# Author:houyafan
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from menu import menu
from core.data.CONST import BASE_PATH,DATA_PATH
from core.takeDeposit.takeNow import *
from core.modifyDeposit.modifyDeposit import *
from core.menu.menu import *
from core.login.login import *
def main():
    menu() # 0 为入口标识  0是商场  1是Atm
main()



'''
取现计算公式：输入的金额等于 金额+金额*0.05
    需要增加余额概念 防止还款超过信用额度
    增加装饰器判断是否已登录
还款：
1、不欠
    直接增加用户余额
2、欠款
    2.1 还款等于欠款：额度变为15000
    2.2 还款大于欠款：额度变为15000，余额增加，新余额等于 余额+还款数-欠款数
    2.3 还款数小欠款数：
         有余额：
            余额+还款数大于欠款数，额度变为15000，余额变为
         没有余额：新额度等于额度加还款金额
'''