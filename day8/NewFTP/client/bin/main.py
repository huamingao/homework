#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from conf.conf import *
from src import user

def main():
    while True:
        option = input(WEL_INFO)
        if option == '3':
            exit()
        elif option == '1':
            user.User.login()
        elif option == '2':
            user.User.register()
        else:
            print(INVALID_INPUT)

if __name__ == '__main__':
    main()
