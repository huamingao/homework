#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao
'''
问题：
1、BUG：当输入的选项不存在时候会出现如下的错误，字典有has_key方法可以做判断，
Traceback (most recent call last):
    请输入菜单名，以进入子菜单；
  File "D:/51CTO学员作业/高华敏/day1/multiMenu/multiMenu.py", line 58, in <module>
    退出，请输入q；返回上层，请输入b
    resList = msg(layer,option)
    -----------------------------------
  File "D:/51CTO学员作业/高华敏/day1/multiMenu/multiMenu.py", line 32, in msg

    return dic[option].keys()
KeyError: '上海'
2、每次输入的都是全名，有没有更好的方式
比如输入1、2、4这样数字，简化操作
3、这种实现三级菜单的方式，太独特了，不过感觉有点乱，有更好的方式哦

'''

# 初始字典
DIC = {
    '北京':{
        '朝阳':{
            '望京':['索尼','360','Alibaba'],
            '国贸':['CCTV','英孚教育']
        },
        '昌平':{
            '天通苑':['链接地产','我爱我家'],
            '沙河':['老男孩']
        }
    },
    '武汉':{
        '武昌':{
            '南湖':['中原地产'],
            '光谷':['斗鱼','HP','德电']
        },
        '汉阳':{
            '四新':['神龙汽车'],
            '沌口':['东风日产','马应龙']
        }
    }
}


# 全局常量
WEL_MSG = '欢迎来到三级菜单,您所在的当前菜单选项如下'.center(35,'*')
RULE_MSG = '''
*************************************************
进入子菜单，请输入相应代码；退出，请输q；返回上层，请输b
*************************************************
'''

# 变量
option = ''
current_dic = DIC

# 函数，传入当前字典和本次输入的编号option，返回内嵌的下一级字典
def get_embed_dic(current_dic,option):
    # 获取当前字典的所有键的值，将它们放入列表
    values_list = list(current_dic.values())
    # 根据编号option 获取对应类目/商品所在的索引位置
    index = int(option) - 1
    current_dic = values_list[index]
    return current_dic

# 函数，根据当前字典和初始字典，返回当前字典的上一级字典
def get_upper_dic(current_dic):
    if type(current_dic) == list:
        for subdic in DIC.values():
            for sub_subdic in subdic.values():
                for embed_list in sub_subdic.values():
                    if current_dic == embed_list:
                        current_dic = sub_subdic
    for item in DIC.values():
        if item == current_dic:
            current_dic = DIC
    for subdic in DIC.values():
        for item in subdic.values():
            if item == current_dic:
                current_dic = subdic
    return current_dic


# 主程序
while option != 'q':

    # 打印欢迎信息
    print(WEL_MSG)

    # 打印当前字典（菜单）
    for i, item in enumerate(current_dic):
        print(i + 1, item)
    print(RULE_MSG)

    # 如果当前菜单达到最内层（最内层是列表），打印提示
    if type(current_dic) == list:
        print('\033[31;1m已经到了最底层，退出请输q，返回上层请输b！\033[0m')

    option = input('请输入你的选择：')

    # 如果输入q，退出程序
    if option == 'q':
        print('\033[31;1m你已成功退出程序！\033[0m')
        exit()

    # 如果输入b
    if option == 'b':
        # 如果当前字典是初始字典，即当前位置是顶层，打印提示
        if current_dic == DIC:
            print('\033[31;1m已经到了最顶层，退出请输q,进入下层请输代码！\033[0m')
            continue
        # 如果当前不在最顶层，调用get_upper_dic函数获取上一层级的字典
        else:
            current_dic = get_upper_dic(current_dic)

    # 如果当前层级不是最底层，且输入option值存在于当前层级列表中，获取下一级字典，进入下次循环
    if type(current_dic) == dict and int(option) in range(len(current_dic.keys())+1):
        # 调用get_embed_dic函数获取下一层级的字典
        current_dic = get_embed_dic(current_dic,option)
    else:
        print('\033[31;1m输入不合法，请重新输入！\033[0m')






