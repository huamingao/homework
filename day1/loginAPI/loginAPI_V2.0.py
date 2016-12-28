#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import getpass

#常量
FILE = 'credential'
COUNTER = 3
STATUS = ['active','locked']

# 空字典，用于储存文件FILE中的数据
dictUsr = {}

# 函数，传入文件名，以文件内容构建字典，返回字典
def mkDict(file):
    if not os.path.exists(file):
        open(file, 'w').close()
    else:
        with open(file, 'r') as f:
            dictUsr = {}
            for line in f.readlines():
                if line != '\n' :
                    usr = line.split(':')[0]
                    pwd = line.split(':')[1]
                    status = line.split(':')[2]
                    dictUsr[usr] = [pwd,status]
    return dictUsr


# 函数，传入文件名、字典，将字典中的数据格式化写入到文件中
def dictToFile(file,dictUsr):
    with open(file, 'w') as f:
        for usr, pwdStat in dictUsr.items():
            seq = (usr,pwdStat[0],pwdStat[1],'\n')
            line = ':'.join(seq)
            f.write(line)

# 函数，传入字典，待检测的用户名usr，输错次数上限值cnt。计数器初始值为0
# 提示用户输入密码，若输入正确，打印欢迎信息并终止，若输错，打印输错信息，
# 循环输入密码，直到输错次数达到cnt值，返回计数器的值
def counter(dictUsr,usr,cnt):
    counter = 0
    while counter < cnt:
        pwd = getpass.getpass('input password:')
        if dictUsr[usr][0] == pwd:
            print('Welcome!You login!')
            break
        else:
            print('Wrong password!Please retype:')
            counter += 1
    return counter

# 主函数
# 构建字典实例
dictUsr = mkDict(FILE)
username = input('input username:')
# 如果用户存在字典中
if username in dictUsr.keys():
    # 取状态值，若值等于常量COUNTER，打印账号被锁定，退出程序
    if dictUsr[username][1] == STATUS[1]:
        print('Account has been locked out!')
    else:
        # 调用函数counter,若输错密码次数达到COUNTER值，打印锁定信息，并将字典中用户状态置为常量STATUS的值
        if counter(dictUsr,username,COUNTER) == COUNTER:
            print('%d times achieved!Account locked out' % COUNTER)
            dictUsr[username][1] = STATUS[1]
# 如果用户不在字典中，提示输入初始密码，并存入字典，以便下次登录
else:
    print('Account not exist!')
    passwd = getpass.getpass('input initial password for next login:')
    dictUsr[username]=[passwd,STATUS[0]]
#把更新好的字典写入文件
dictToFile(FILE,dictUsr)



