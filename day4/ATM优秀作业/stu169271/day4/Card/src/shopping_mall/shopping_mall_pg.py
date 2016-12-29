#!/usr/bin/env python
# encoding: utf-8


import os
import datetime
import json

login_log = "../log/login.log"                     # 用户登录系统日志
password_file = "../db/passwd.txt"                # 用户认证文件
lock_file = "../db/lock_account.txt"              # 被锁定用户被存入该文件
color_end = "\033[0m"
color_red = "\033[31;1m"
color_green = "\033[32;1m"
today = datetime.datetime.today().strftime("%Y:%m:%d %H:%M:%S")
today_day = datetime.datetime.today().strftime("%Y:%m:%d")

# os.system('cls')                               # window和linux兼容问题去掉

'''
   商品信息
'''
product_dict = {
    '家用电器': {
        '生活电器': [('电风扇', 355), ('饮水机', 150)],
        '五金家装': [('水槽', 20), ('电器开关', 30)]
    },
    '手机数码': {
        '手机通讯': [('XiaoMi 2', 999), ('Apple 6 Pluse', 6666)],
        '影音娱乐': [('音响', 2000), ('收音机', 100)],
    }
}

province_dict = {}          # 商品大类
city_dict = {}              # 商品小类
county_dict = {}            # 商品信息


def log_w(file_name, text):
    """
    进行文件日志记录
    :param result_name: 将内容记录到该文件中
    :param text: 要进行记录的内容
    :return: 默认值None
    """
    f_name = "%s" % file_name
    f_log = open(f_name, "a+")
    f_log.write(text)
    f_log.close()


def store(username, user_info_dict):
    """
    保存用户的余额信息 保存格式：每个用户一个json格式的文件，例如账号名称为lln,则文件为lln_info.json
    :param username: 接受用户名
    :param user_info_dict: 接受用户的字典信息
    :return: 无返回值
    """
    user_info_file = username + '_info.json'
    with open(user_info_file, 'w') as json_file:
        json_file.write(json.dumps(user_info_dict))


def load(username):
    """
    用于获取用户余额信息
    :param username: 接受用户的用户名
    :return: 返回用户存储的信息字典格式
    """
    user_info_file = username + '_info.json'
    with open(user_info_file) as json_file:
        data = json.load(json_file)
        return data


def register():
    """
    用户注册功能
    :return:
    """
    username_list = []
    print("账号注册".center(50, "-"))
    username = input("请输入用户名:")
    password = input("请输入密码:")           # 隐藏输入的密码信息
    with open(password_file, 'r') as pas:
        for user_list in pas.readlines():
            user_name, user_pass = user_list.strip('\n').split()
            username_list.append(user_name)
    if username_list.count(username) == 0:
        text = "%s %s\n" % (username, password)
        log_w(password_file, text)
        print(color_green+"账号注册成功"+color_end)
    else:
        print("该用户名已经被注册")


def show_province():
    print("一级菜单信息".center(50, "-"))
    for index, province in enumerate(product_dict, 1):  # 遍历字典的key，列出一级省份名字
        province_dict[index] = province
    for index in province_dict:
        print(index, ".", province_dict[index])


def show_city(choice_provice):
    print("二级菜单信息".center(50, "-"))
    for index, city in enumerate(product_dict[province_dict[choice_provice]].keys(), 1):
        city_dict[index] = city
    for index in city_dict:
        print(index, ".", city_dict[index])
    print('>>', province_dict[choice_provice])


def show_county(choice_provice, choice_city):
    print("三级菜单信息".center(50, "-"))
    for index, county in enumerate(product_dict[province_dict[choice_provice]][city_dict[choice_city]], 1):
        county_dict[index] = county
    for index in county_dict:
        print(index, ".", county_dict[index])
    print('>>', province_dict[choice_provice], '>>', city_dict[choice_city])


def login_menu():
    """
    系统登录注册函数
    :return:
    """
    msg = '''
#########################################
           欢迎登陆本商城
             1.用户注册
             2.登陆
             3.退出
#########################################
           作者:kuangmeilin
           时间：%s
#########################################
    ''' % today_day
    while True:
        print(color_green, msg, color_end)
        input_num = input("请选择:")
        if input_num.strip().isdigit():         # 过滤用户输入内容中的空格，然后判断内容是否是数字
            input_num = int(input_num)
        if input_num == 1:
            register()                          # 调用用户注册函数
        elif input_num == 2:
            # 用户登录功能
            count = 0
            flag = True
            while flag:
                if count < 3:                                            # 只要重试不超过三次就不断循环
                    username = input("请输入用户名:")
                    password = input("请输入密码:")
                    # 判断账号是否在锁定列表中，如果已经被锁定过，直接退出程序
                    with open(lock_file, 'r') as pas:
                        for line in pas.readlines():
                            if username in line:
                                print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
                                text = "%s user login is locked at %s\n" % (username, today)
                                log_w(login_log, text)
                                flag = False
                                break

                    # 判断账号及密码是否在password.txt文件中存在且正确，如果正确记录日志，输出登录信息
                    with open(password_file, 'r') as pas:
                        for line in pas.readlines():
                            user, passwd = line.strip('\n').split()  # 去掉每行多余的\n并把这一行按空格分成两列，分别赋值为user,passwd两个变量
                            if username == user and password == passwd:
                                text = "%s user login successfully at %s\n" % (username, today)
                                log_w(login_log, text)

                                # shopping_mall()  商城功能开始
                                exit_flag = False
                                shop_car = []

                                user_info_file = username + '_info.json'
                                if os.path.exists(user_info_file):       # 判断用户信息文件是否存在，存在则根据信息文件初始化余额信息
                                    user_info_dict = load(username)
                                    salary_balance = user_info_dict.get(username)[0]
                                    salary = salary_balance
                                else:          # 判断用户信息文件是否存在，不存在则属于第一次登录，初始化用户信息
                                    salary = 0
                                    user_info_dict = {username: [salary, today]}  # 构造一个python对象
                                    store(username, user_info_dict)

                                last_time = user_info_dict.get(username)[1]

                                welcome_msg = '''
#########################################
          欢迎登陆本商城系统
           1.选择菜单
           2.返回上一级菜单
           3.充值
           4.查看购物车
           5.绑定信用卡
           6.退出
#########################################
           作者：kuangmeilin
           时间：%s
#########################################
用户名：%s 余额：%s 上次登录时间：%s
                                ''' % (today_day, username, salary, last_time)
                                while exit_flag is not True:
                                    print(color_green + welcome_msg + color_end)
                                    input_num = input("请选择:")
                                    if input_num.strip().isdigit():  # 过滤用户输入内容中的空格，然后判断内容是否是数字
                                        input_num = int(input_num)
                                    if input_num == 1:
                                        show_province()
                                        choice_provice = input("请选择商品大类:")
                                        if choice_provice.strip().isdigit():
                                            choice_provice = int(choice_provice)
                                            if choice_provice not in province_dict:
                                                print('请输入一个有效的号码!')
                                                continue
                                            else:
                                                show_city(choice_provice)

                                        choice_city = input(color_green+"[退出：q,返回：b]"+color_end+"请选择商品小类：")
                                        if choice_city.strip().isdigit():
                                            choice_city = int(choice_city)
                                            if choice_city not in city_dict:
                                                print('请输入一个有效的号码!')
                                                continue
                                            elif choice_city == "b":
                                                show_province()
                                            elif choice_city == "q":
                                                break
                                            else:
                                                province_list = show_county(choice_provice, choice_city)
                                        # 购买程序
                                        # print(county_dict)
                                        user_choice = input("[退出（q=quit）,查看购物车（c=check）,充值（a=recharge）]请输入要购买的商品编号:")
                                        if user_choice.isdigit():
                                            user_choice = int(user_choice)
                                            user_choice_num = input("请输入购买商品数量:")
                                            if user_choice_num.strip().isdigit():
                                                user_choice_num = int(user_choice_num)
                                            # print(user_choice,user_choice_num)
                                            if user_choice < len(county_dict):
                                                p_item = county_dict[user_choice]  # 根据用户选择的商品ID获取商品价格
                                                if p_item[1] * user_choice_num <= salary:
                                                    p_item = list(p_item)
                                                    p_item.append(user_choice_num)
                                                    shop_car.append(p_item)
                                                    # print(p_item,user_choice_num,shop_car)  # ['音响', 2000, 1]
                                                    # {['商品名称', 单价, 数量],['商品名称',单价, 数量]}
                                                    salary -= p_item[1] * user_choice_num
                                                    for index, i in enumerate(shop_car):
                                                        print(
                                                         "您购买的商品：[%s]，单价：[%s]，数量：[%s],已经加入购物车,"
                                                         "您的账号余额为：\033[31;1m[%s]\033[0m" % (
                                                             i[0], i[1], i[2], salary))
                                                    user_info_dict = {username: [salary, today]}
                                                    store(username, user_info_dict)
                                                else:
                                                    print("Your balance is [%s],cannot afford this.." % salary)
                                    elif input_num == 2:
                                        pass
                                    elif input_num == 3:
                                        user_info_dict = load(username)  # 获取用户余额信息
                                        salary_balance = user_info_dict.get(username)[0]
                                        salary = salary_balance
                                        print("欢迎进入商城充值中心".center(40, "*"))
                                        print("您好，[%s],您的当前余额为：[%s]" % (username, salary))
                                        recharge_money = input("请输入充值金额：")
                                        if recharge_money.strip().isdigit():
                                            recharge_money = int(recharge_money)
                                        salary += recharge_money
                                        store(username, user_info_dict)    # 充值完成 保存余额信息
                                        print("充值成功，您目前的余额为：\033[41;1m[%s]\033[0m" % salary)
                                        print("完成".center(40, "*"))
                                    elif input_num == 4:
                                        print("商品信息".center(50, "-"))
                                        print("\033[33;1m序列\t商品\t\t商品单价\t商品数量\t总价\033[0m")
                                        for index, i in enumerate(shop_car):
                                            print("\033[33;1m%2d\t\t%-5s\t\t%-5s\t\t%-4s\t\t%-4s\033[0m" % (
                                             index, i[0], i[1], i[2], i[1] * i[2]))
                                        print("余额".center(50, "-"))
                                        print("你的账号余额 [%s]" % salary)
                                        print("结束".center(50, "-"))
                                    elif input_num == 5:
                                        print("实现绑定信用卡功能")
                                    elif input_num == 6:
                                        print("商品信息".center(50, "-"))
                                        print("\033[33;1m序列\t商品\t\t商品单价\t商品数量\t总价\033[0m")
                                        for index, i in enumerate(shop_car):
                                            print("\033[33;1m%2d\t\t%-5s\t\t%-5s\t\t%-4s\t\t%-4s\033[0m" % (
                                             index, i[0], i[1], i[2], i[1] * i[2]))
                                        print("余额".center(50, "-"))
                                        print("你的账号余额 [%s]" % salary)
                                        print("结束".center(50, "-"))

                                        exit_flag = True
                                        user_info_dict = {username: [salary, today]}  # 构造一个python对象
                                        store(username, user_info_dict)               # 退出前保存用户信息

                                    else:
                                        os.system('cls')
                                        print("输入错误")
                                        continue
                                # 商城功能结束
                                flag = False  # 如果账号及密码信息正确，则记录日志，跳出循环
                                break
                            else:
                                continue
                    count += 1
                # 如果同一个账号连续输错三次，则将账号记录到锁定文件列表，并退出程序
                else:
                    print(color_red + "你已经连续三次输出，账号被锁定" + color_end)
                    text = "%s user login is locked at %s\n" % (username, today)
                    log_w(login_log, text)
                    text = "%s\n" % username
                    log_w(lock_file, text)
                    flag = False
        elif input_num == 3:                    # 退出系统
            break
        else:
            os.system('cls')
            print("输入错误")
            continue


def shopping_mall_main():
    login_menu()

if __name__ == '__main__':
    shopping_mall_main()
