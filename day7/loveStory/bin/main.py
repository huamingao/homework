#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import pickle
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from src.user import User
from src.poor import Poor


INTRODUCTION = '''
欢迎来到模拟人生游戏剧场！

剧情提要：
大学时，你是一位屌丝。通过努力，女神Liz成为了你的恋人。毕业后，Liz傍上高富帅Peter。
多年后，你也成了高富帅，遇到被甩的Liz，Liz向你提出复合，你该如何抉择...'''
MAIN_MENU = '''
1 登录
2 注册新玩家
请输编号继续，退出请输q:'''


if __name__ == "__main__":
    print(INTRODUCTION)
    while True:
        option = input(MAIN_MENU)
        if option == 'q':
            exit()
        elif option == '1':
            Poor.login()
        elif option == '2':
            Poor.register()
        else:
            print('您输入的选项不存在，请重新输入！')








