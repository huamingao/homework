# Author:houyafan
import json, os,time, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.data.CONST import BASE_PATH,DATA_PATH


# 获取当前登陆用户名
def get_username():
    with open(DATA_PATH+"username.txt","r")as f:
        user=f.read()
    return user

# username = get_username() # 获取用户名


# 通用的写log方法 传文件句柄 数据源
def write_log(f,data):
    f.seek(0)
    f.truncate()
    f.write(json.dumps(data))
    f.flush()
    f.close()


# 写入账单的全局方法 需要传 文件句柄 账单文案 数据源
def public_write(f,info,data):
    username = get_username()
    month_time = time.strftime("%m", time.localtime())
    if username not in data.keys():
        data[username] = {}
        if month_time not in data[username].keys():
            data[username][month_time] = []
            data[username][month_time].append(info)
            write_log(f, data)
        else:
            data[username][month_time].append(info)
            write_log(f, data)
    else:
        if month_time not in data[username].keys():
            data[username][month_time] = []
            data[username][month_time].append(info)
            write_log(f, data)
        else:
            data[username][month_time].append(info)
            write_log(f, data)


# 写入还款金额
def write_file(f, data):
    username = get_username()
    write_log(f, data)
    print("还款成功,信用卡额度剩余\033[31;1m%s\033[0m元...余额\033[31;1m%s\033[0m元..." % (
    data[username]["message"]["CreditMax"], data[username]["message"]["Balance"]))
    f.close()


# 写入结算金额
def write_modify_file(f, data):
    username = get_username()
    write_log(f, data)
    print("结账成功，余额剩余\033[31;1m%s\033[0m元，信用额度剩余\033[31;1m%s\033[0m元" % (
        data[username]["message"]["Balance"], data[username]["message"]["CreditMax"]))


# 写入取现金额
def write_take_money(f,data,procedure):
    username = get_username()
    write_log(f, data)
    print("取现成功，余额剩余\033[31;1m%s\033[0m元，信用额度剩余\033[31;1m%s\033[0m元,手续费\033[31;1m%s\033[0m元" % (
        data[username]["message"]["Balance"], data[username]["message"]["CreditMax"],procedure))
    f.close()


# 写入转账金额
def write_turn_money(f,data,turn_username,price):
    write_log(f,data)
    print("转账成功,转账给 %s ,转账金额 %s"% (turn_username,price))
    f.close()


# 公共的退出方法 (只需要传文件路径就可以)
def logout(file_path):
    username = get_username()
    with open(file_path, 'r+')as f:
        data = json.load(f)
        data[username]["message"]['status'] = 3
        write_log(f, data)
    print("\033[33;1m谢谢使用\033[0m".center(50, '*'))
    with open(DATA_PATH + "username.txt", 'w')as f:
        pass


