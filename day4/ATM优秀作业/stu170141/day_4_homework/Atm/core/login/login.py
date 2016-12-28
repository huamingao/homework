# Author:houyafan
import os, sys, json
from core.data.CONST import BASE_PATH, DATA_PATH
from core.tools.check import *


def loginAtm():
    count = 0
    while True:
        username = input("请输入您的账号：")
        password = input("请输入您的密码：")
        if check_username(username, password):
            continue
        else:
            with open(DATA_PATH + 'card_message_tmp.json')as f:
                data=json.load(f)
            if username in data.keys():
                if count >= 3 or data[username]["message"]['status'] == 2:
                    data[username]["message"]['status'] = 2 # 状态0为成功 1为失败 2为冻结 3为退出
                    with open(DATA_PATH + 'card_message_tmp.json','w') as f:
                        f.write(json.dumps(data))
                    exit("您的银行卡已被冻结，请到营业厅办理解卡！！")
                    return False
                elif password == data[username]["message"]["password"]:
                    print("\033[32;1m登陆成功\033[0m".center(50, '*'))
                    data[username]["message"]['status'] = 0 # 状态0为成功 1为失败 2为冻结 3为退出
                    with open(DATA_PATH + 'card_message_tmp.json','w') as f:
                        f.write(json.dumps(data))
                    with open(DATA_PATH+"username.txt","w")as f:
                        f.write(username)
                        f.flush()
                    return True

                else:
                    print("\033[31;1m账号或密码错误，请重新输入！！\033[0m")
                    count += 1
                    continue
            else:
                print("没有这个用户")