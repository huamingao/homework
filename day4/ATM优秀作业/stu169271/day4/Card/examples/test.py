#!/usr/bin/env python
# encoding: utf-8




import sys
import os

# lib_path = os.path.abspath('../lib')
# sys.path.append(lib_path)

#
import pickle
#
# # card_user_info_dict = {'11': 22}
# # pickle.dump(card_user_info_dict, open('../db/user_info.pickle', 'wb'))
#
card_user_info_dict = pickle.load(open('../db/user_info.pickle', 'rb'))  # 获取原有的用户信息
print(card_user_info_dict)


# from commons import md5
#
# pass_word = 'aaa'
# res = md5(pass_word)
# print(res)

# card_cash_sum = 100
# sa =card_cash_sum * 0.05
# print("取现成功，取现手续费%.2f元" % sa)
#
# a = input("s")
# a = float(a)
# print(a, type(a))

# card_user_info_dict = {}
# admin_info = {}
# admin_info["user_name"] = 'admin'
# admin_info["account_name"] = 'admin'
# admin_info["password"] = '123'
# card_user_info_dict['admin'] = admin_info
#
# print(card_user_info_dict)

# import logging
# log_file = '../1.log'
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=log_file,
#                     filemode='w')
#
# logging.debug('debug message')
# # logging.info('info message')
# # logging.warning('warning message')
# # logging.error('error message')
# # logging.critical('critical message')

import os
lock_file = "../lock_account.txt"

def file_is_exist(filename):
    if os.path.exists(filename):
        message = "True"
    else:
        message = "False"
    return message


res = file_is_exist(lock_file)  # 判断用户锁文件是否存在，不存在创建
if res == "False":
    open(lock_file, "w+").close()