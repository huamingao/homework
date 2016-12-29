#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import getpass
import time

# 全局常量
FILE = 'shopcart.txt'
COUNTER = 3
STATUS = ['active','locked']

# 存储要打印的信息
WEL_MSG = '欢迎来到我的商城！'.center(50, '*')
ACHEIVE_TOP_MSG = '\033[31;1m您已来到顶级类目！\033[0m'
LIST_MSG = '若要进入子类目，请输入对应的编号！\n'
CURRENT_CATEGORY_MSG = '您已来到类目：'
ACHEIVE_EMBED_MSG = '您已到达商品价格列表！若要购买，请输入相应的商品编号！'
FAIL_BACK_MSG = '\033[31;1m无法返回上层！\033[0m'
EXIT_PROMPT = '\033[31;1m你已成功退出程序！\033[0m'
PURCHASE_MSG = '\033[31;1m以下商品已成功加入购物车:\033[0m'
MONEY_MSG = '\033[31;1m当前余额：\033[0m'
NOMONEY_MSG = '\033[31;1m，您的余额不充足\033[0m'
CHARGE_MSG = '\033[31;1m您已成功充值！\033[0m'
MENU_MSG = '编号 商品 价格'
INVALID_MSG = '\033[31;1m您的输入不合法，请重新输入！\033[0m'
RULE_MSG = '''
\033[31;1m规则：退出，请输q；返回上层，请输b；查看购物车，请输c；钱包充值，请输a\033[0m
*******************************************************************
'''
SHOPCART_MSG = '''
********以下是您已购入的商品********
--------------------------------
编号 商品 单价 数量 总价 上次购买时间
'''

# 存储交互式输入时的提示语
OPTION_PROMPT = '请输入您的选择：'
QUANTITY_PROMPT = '\033[31;1m请输入您要购买的商品数量：\033[0m'
MONEY_PROMPT = '\033[31;1m请您输入要充入的金额：\033[0m'
CONTINUE_BUY_PROMPT = '\033[31;1m退出整个程序请输q，若要继续购物，请输入非q的任意键：\033[0m'

# 商品列表
PRODUCT_DIC = {
    '家电':{
        '洗衣机':{
            '海尔':3000,
            '美诺':5000,
            'TCL':2000
        },
        '冰箱':{
            '容声':2000,
            '美的':3000
        }
    },
    '手机':{
        'IPhone':{
            'IPhone7':7000,
            'IPhone6':5000,
            'IPhone5':3999
        },
        '小米':{
            '小米3':2000,
            '红米2':1500
        }
    },
    '服饰':{
        'H&M':{
            '牛仔裤':300,
            'T恤衫':100,
            '袜子':20
        },
        'Zara':{
            '风衣':900,
            '连衣裙':400,
            '帽子':80
        }
    }
}

option = ''
cost = 0


# 函数，文件file记录购物车历史信息，以文件内容构建形如{usr:[pwd,stat,money,{productA:[quantity,last_purchase_time]},...}的字典
def mkdict(shopcart_file):
    # 如果文件不存在，就先创建一个空文件
    if not os.path.exists(shopcart_file):
        open(shopcart_file, 'w').close()
        return {}
    else:
        with open(shopcart_file,'r',encoding='UTF8') as f:
            # 局部变量dic，字典，存储所有人的所有已购商品信息
            dic = {}
            # 对文件中每一行逐行进行操作
            for line in f.readlines():
                # 局部变量shopcart，列表，存储单个用户的所有已购商品信息
                shopcart = []
                # 跳过空行，只对非空行操作
                if line != '\n' :
                    # 获取用户名、密码、账号状态、余额，构建字典dic
                    usr = line.split(':')[0]
                    pwd = line.split(':')[1]
                    stat = line.split(':')[2]
                    money = line.split(':')[3].split('\n')[0]
                    money = int(money)
                    dic[usr] = [pwd, stat, money]
                    # 如果该行用户的购物车不为空，构建shopcart购物车信息
                    if line.split(':')[4:] != []:
                        # 对当前行切片，构建shopcart，是一个由N条商品信息组成的列表，
                        # 每条商品信息都是一个形如{product:[quantity,last_purchase_time]}的字典
                        for item in line.split(':')[4:]:
                            # 取商品名
                            product_name = item.split('*')[0]
                            # 取商品数量，并转换为整型
                            quantity = int(item.split('*')[1])
                            # 取时间戳，并转换为浮点型
                            last_purchase_time = float(item.split('*')[2].split('\n')[0])
                            # 局部变量product_info，字典，存储单个用户的单个已购商品信息
                            product_info = {product_name:[quantity,last_purchase_time]}
                            # 将单个商品信息追加到列表shopcart中
                            shopcart.append(product_info)
                        dic[usr].extend(shopcart)
        return dic


# 函数，将字典中的数据格式化写入文件（覆盖写），该文件存储购物车历史信息
def dicttofile(shopcart_file,dic):
    with open(shopcart_file, 'w',encoding='UTF8') as f:
        # 对字典中的每个key即每个用户逐个处理
        for key in dic.keys():
            # 取得当前用户的用户名、密码、账号状态、余额
            usr = key
            pwd = dic[usr][0]
            stat = dic[usr][1]
            money = str(dic[usr][2])
            # 为当前用户拼接字符串，以便在此轮循环的最后将该行写入文件
            seq = [usr,pwd,stat,money]
            # 如果该用户的购物车不为空
            if dic[usr][3:] != []:
                # 定义一个列表，用于存储当前用户购物车中的所有商品信息
                all_product_info = []
                # 对该用户购物车中的所有商品，依次逐个步骤
                for product_info in dic[usr][3:]:
                    # 取购物车中当前商品的商品名、商品数量、购买时间
                    product_name = list(product_info.keys())[0]
                    quantity = product_info[product_name][0]
                    last_purchase_time = product_info[product_name][1]
                    # 将当前商品的三项信息存入一个列表
                    seq_product = [product_name,str(quantity),str(last_purchase_time)]
                    # 将该列表元素以*拼接成字符串，称为当前商品信息字符串
                    str_product_info = '*'.join(seq_product)
                    # 将当前商品信息字符串添加到列表，该列表存储当前用户的所有商品信息
                    all_product_info.append(str_product_info)
                seq.extend(all_product_info)
            line = ':'.join(seq)
            line = line + '\n'
            f.write(line)


# 函数，传入当前字典和本次输入的编号option，返回内嵌的下一级字典
def get_embed_dic(current_dic,option):
    # 获取当前字典的所有键的值，将它们放入列表
    values_list = list(current_dic.values())
    # 根据编号option 获取对应类目/商品所在的索引位置
    index = int(option) - 1
    current_dic = values_list[index]
    return current_dic


# 函数，根据当前菜单和初始菜单，返回上一级菜单（字典）
def get_upper_dic(init_dic, current_dic):
    for item in init_dic.values():
        if item == current_dic:
            current_dic = init_dic
    for subdic in init_dic.values():
        for item in subdic.values():
            if item == current_dic:
                current_dic = subdic
    return current_dic


# 要求用户输入一串数字，输错打印'输入不合法'，直至输入合法为止
def input_isdigit(msg_prompt,invalid_msg):
    while True:
        input_msg = input(msg_prompt)
        if not input_msg.isdigit():
            print(invalid_msg)
        else:
            break
    return input_msg


# 函数，登录模块，通过调用函数mkdict读取文件内容，若账号存在，检查账号状态: 若状态为被锁定，返回[False,username]；
# 否则，提示输入密码，输入正确返回[True,username]，输错密码达到3次，锁定账号，通过调用函数dicttofile更新文件，返回[False,username];
# 若账号不存在，提示输入初始密码、初始金额，通过调用函数dicttofile更新文件，返回[True,username]
def login(file):
    # 局部常量，存储交互式输入时的提示语
    USR_PROMPT = '请输入您的用户名:'
    PWD_PROMPT = '请输入您的密码:'
    INIT_PWD_PROMPT = '请输入初始登录密码:'
    INIT_MONEY_PROMPT = '请输入您钱包中的初始金额:'

    # 局部常量，存储要打印的信息
    WRONG_PWD_MSG = '密码错误！请您重新输入!'
    WEL_MSG = '\033[31;1m欢迎来到我的商城！您的当前余额：\033[0m'
    LOCKED_MSG = '\033[31;1m您的账号已被锁定，请联系管理员解锁!\033[0m'
    CNT_LOCKED_MSG = '\033[31;1m您已输错%d次，%s\033[0m' % (COUNTER,LOCKED_MSG)
    USR_NOEXIST_MSG = '\033[31;1m您是新用户!请按以下步骤完成首次登陆！\033[0m'


    # 调用mkdict函数，利用文件内容构建字典，存储所有用户的购物车信息
    all_user_shopcart = mkdict(file)
    username = input(USR_PROMPT)

    # 如果用户存在
    if username in all_user_shopcart.keys():
        money = all_user_shopcart[username][2]
        # 取状态值，若为Locked，打印账号被锁定，退出程序
        if all_user_shopcart[username][1] == STATUS[1]:
            print(LOCKED_MSG)
            return False,username

        # 若输入密码正确，返回True；否则提示重新输入，直至输错次数达到上限值COUNTER
        counter = 0
        while counter < COUNTER:
            pwd = input(PWD_PROMPT)
            if all_user_shopcart[username][0] == pwd:
                print(username,WEL_MSG,money,'\n')
                return True,username
            else:
                print(WRONG_PWD_MSG)
                counter += 1

        # 输错次数达到上限，打印账号锁定信息，并将字典中用户状态置为STATUS[1]即locked，将更新写入文件，返回False
        if counter == COUNTER:
            print(CNT_LOCKED_MSG)
            # 更新该用户的账号状态信息为locked
            all_user_shopcart[username][1] = STATUS[1]
            # 将更新过的字典写入文件
            dicttofile(FILE, all_user_shopcart)
            return False,username

    # 如果用户不在字典中，提示输入初始密码，并存入字典后返回True
    else:
        print(USR_NOEXIST_MSG)
        passwd = input(INIT_PWD_PROMPT)
        money = int(input_isdigit(INIT_MONEY_PROMPT,INVALID_MSG))
        # 把新用户的信息（账号名、密码、账号状态、初始金额）作为字典的新增键值对，加入字典
        all_user_shopcart[username]=[passwd,STATUS[0],money]
        # 将更新过的字典写入文件
        dicttofile(FILE,all_user_shopcart)
        return True,username

# 函数，根据商品编号，从商品字典中获取商品名，并返回
def get_product_name(product_dic, option):
    keys = product_dic.keys()
    index = int(option) - 1
    product_name = list(keys)[index]
    return product_name


# 函数，根据商品名，从商品字典中获取商品单价，并返回
def get_price(product_dic,product_name):
    for sub_menu_list in product_dic.values():
        for subdic in sub_menu_list:
            if product_name in sub_menu_list[subdic].keys():
                product_price = sub_menu_list[subdic][product_name]
                break
    return product_price


# 函数，打印当前用户的已购入商品信息（商品，数量，最后一次购买时间）
def print_shopcart(all_user_shopcart,username):
    # 取得当前用户的用户名、余额
    usr = username
    money = all_user_shopcart[username][2]
    print('%s,%s' % (usr,SHOPCART_MSG))
    i = 1
    for product_info in all_user_shopcart[username][3:]:
        # 取购物车中当前商品的商品、单价、数量、总价、上次购买时间
        product_name = list(product_info.keys())[0]
        product_price = get_price(PRODUCT_DIC,product_name)
        quantity = product_info[product_name][0]
        cost = product_price * quantity
        last_purchase_time = product_info[product_name][1]
        # 购买时间是时间戳格式，将其转换为易读格式:
        timeArray = time.localtime(last_purchase_time)
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 按以下顺序打印：'编号 商品 单价 数量 总价 上次购买时间'
        print('%d   %s   %d  %d  %d  %s' %(i,product_name,product_price,quantity,cost,format_time))
        i += 1
    print(MONEY_MSG,money)

# 主程序
# 调用login函数，返回值是形如[布尔值,username]的列表，将其存入res_login
res_login = login(FILE)
# 获取所有用户的购物历史信息，这行必须放在登录模块后面，确保如果是新用户登录，all_user_shopcart里面会包括信用户的信息
all_user_shopcart = mkdict(FILE)
# 如果返回的布尔值为False，说明登录失败，直接退出程序
if not res_login[0]:
    exit()
# 如果登录成功
else:
    # 获取当前用户名
    username = res_login[1]
    # 打印欢迎信息
    print(WEL_MSG)
    # 声明当前层级对应的字典，初始值为顶层字典
    current_product_list = PRODUCT_DIC
    print(ACHEIVE_TOP_MSG,LIST_MSG)
    while option != 'q':
        # 获得当前用户钱包中的金额
        money = all_user_shopcart[username][2]
        # 打印菜单栏'编号 商品 价格'
        print(MENU_MSG)
        # 只要输入不为q，就打印当前菜单中的商品列表
        for i, product in enumerate(current_product_list):
            #如果到达位于最底层的商品价格列表，打印编号、商品、价格
            if type(current_product_list[product]) == int:
                print(i + 1, product, current_product_list[product])
            # 否则，只打印编号、商品类目
            else:
                print(i + 1, product)
        print(RULE_MSG)
        # 如果当前已达到商品价格列表，打印提示'已达到商品价格列表，请选择要购买的商品'
        if type(current_product_list[product]) == int:
            print(ACHEIVE_EMBED_MSG)
        # 提示用户输入选项
        option = input(OPTION_PROMPT)

        if option == 'q':
            # 退出程序前，调用print_shopcart函数，打印已购入商品信息
            print_shopcart(all_user_shopcart,username)
            dicttofile(FILE,all_user_shopcart)
            print(EXIT_PROMPT)
            exit()
        # 如果输入c,调用print_shopcart函数，打印已购入商品信息
        elif option == 'c':
            print_shopcart(all_user_shopcart,username)
            option = input(CONTINUE_BUY_PROMPT)
        # 如果输入b，且当前菜单不是顶层菜单，则返回上级菜单
        elif option == 'b':
            if current_product_list != PRODUCT_DIC:
                current_product_list = get_upper_dic(PRODUCT_DIC,current_product_list)
            # 如果当前处于商城最顶层，打印提示
            else:
                print(ACHEIVE_TOP_MSG,FAIL_BACK_MSG)
                option = input(CONTINUE_BUY_PROMPT)
                print(WEL_MSG)
        # 如果输a，对余额充值

        elif option == 'a':
            money += int(input(MONEY_PROMPT))
            all_user_shopcart[username][2] = money
            print(CHARGE_MSG)
            print(MONEY_MSG,money)
            option = input(CONTINUE_BUY_PROMPT)
        # 如果输入的option存在于当前菜单编号列表中
        elif option.isdigit() and int(option) in range(len(current_product_list.keys())+1):
            # 如果当前菜单的下一级就是商品价格列表（最底层的价格是整型，基于此做判断）
            if type(current_product_list[product]) == int :
                product_name = get_product_name(current_product_list, option)
                # 提示输入要购买的商品数量，调用input_isdigit函数强制必须输入数字
                quantity = int(input_isdigit(QUANTITY_PROMPT, INVALID_MSG))
                # 调用get_price函数获得商品单价，乘以商品数量，计数出总价
                price = get_price(PRODUCT_DIC,product_name)
                cost = current_product_list[product_name] * quantity
                # 如果总价大于余额，提示余额不够
                if cost > money:
                    print(MONEY_MSG,money,NOMONEY_MSG)
                    option = input(CONTINUE_BUY_PROMPT)
                # 否则余额充足，余额减去总价得到新的余额，取出本次购买信息，包括产品、数量，打印购买成功
                else:
                    # 重新计算余额，将更新过的余额写入字典，并打印当前余额
                    money = money - cost
                    all_user_shopcart[username][2] = money
                    print(PURCHASE_MSG, quantity, product,'\n',MONEY_MSG,money)
                    # 获取当前用户的购买记录
                    shopcart = all_user_shopcart[username][3:]
                    # 遍历，判断新购买的商品是否已经存在在以前的购买记录中
                    flag = 0
                    for product_info in shopcart:
                        # 如果购物车中已经存在这件商品，将重新计算出的购买数量更新到shopcart列表中的商品信息里，并将flag置为1
                        if product == list(product_info.keys())[0]:
                            # 重新计算商品数量
                            new_quantity = quantity + product_info[product][0]
                            # 删除shopcart列表中现有的product_info信息
                            shopcart.remove(product_info)
                            # 生成新的product_info，格式如{商品名字：[数量,购买时间]}
                            product_info = {product: [new_quantity, time.time()]}
                            flag = 1
                    # 若遍历shopcart列表后，找不到商品名，即此次购买的商品为新的商品种类
                    if flag != 1:
                        # 生成新的product_info
                        product_info = {product: [quantity, time.time()]}
                    # 将product_info追加到shopcart列表
                    shopcart.append(product_info)
                    # 将新的shopcart更新到all_user_shopcart字典中
                    pwd = all_user_shopcart[username][0]
                    stat = all_user_shopcart[username][1]
                    money = all_user_shopcart[username][2]
                    user_info_shopcart = [pwd,stat,money]
                    user_info_shopcart.extend(shopcart)
                    all_user_shopcart[username] = user_info_shopcart
                    # 调用print_shopcart函数，打印已购入商品信息
                    print_shopcart(all_user_shopcart,username)
                    option = input(CONTINUE_BUY_PROMPT)
            # 如果下一级菜单不是商品价格列表，即仍为商品类目
            else:
                # 根据当前菜单，打印'已来到XX类目'
                for i,item in enumerate(current_product_list.keys()):
                    if i == int(option) - 1:
                        menu = item
                        print(CURRENT_CATEGORY_MSG,menu,LIST_MSG)
                        break
            # 调用get_embed_dic函数，将当前菜单置为下一级菜单，进入下轮循环
                current_product_list = get_embed_dic(current_product_list,option)
        else:
            # 如果用户输入不满足以上条件，打印输入不合法，并提示是否继续购物，获得重新输入的option
            print(INVALID_MSG)
            option = input(CONTINUE_BUY_PROMPT)



