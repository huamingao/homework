import json,os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#当前文件的父级-父级目录--atm目录的绝对路径
sys.path.append(base_dir)
db_path = base_dir + os.path.sep + 'db'+ os.path.sep#db目录的绝对路径
from core import public#从core目录下导入public模块
user_json = base_dir + os.path.sep + 'db' + os.path.sep + 'user.json'#用户信息文件的绝对路径
def login():
    '''登录程序'''
    error_users = [] #记录错误用户信息
    error_count = 0#记录错误次数
    users = public.op_file(user_json)#打开用户信息文件
    while error_count < 3:
        user_name = input("\033[1;36m请输入您的用户名：\033[0m")
        passwd = input("\033[1;36m请输入您的密码：\033[0m")
        if len(user_name)>0:
            user_status = users[user_name]['status']#读取当前用户锁定信息
            if user_name in users:
                if passwd == users[user_name]['passwd'] and user_status == 0:
                    #当前账户密码输入正确且未被锁定，则写入登录状态文件，记录用户信息
                    fw = open(db_path + 'user_status.txt','w')
                    fw.write(user_name)
                    fw.close()
                    return user_name
                elif passwd == users[user_name]['passwd'] and user_status == 1:
                    #当前账户密码输入正确，但已被锁定，给出提示信息
                    print("\033[1;31m用户已被锁定！\033[0m")
                    exit()
                else:
                    error_users.append(user_name)#输入错误则追加错误用户到错误用户文件中
                    print("\033[1;31m用户名或密码输入错误，请重新输入！\033[0m")
                    error_count += 1
                    continue
        else:
            print("\033[1;31m账户不存在，请重新输入！\033[0m")
            continue
    else:
        if error_users.count(user_name) >= 3:#错误文件中某个用户出现的次数大于等于3次，则讲用户文件中该用户的锁定值置为锁定
            users[user_name]['status'] = 1
            fw = public.op_file(db_path + 'user_status.txt')
            fw.seek(0)
            fw.truncate()
            json.dump(users,fw)
            fw.close()
        exit('\033[1;31m失败次数超过3次，程序退出！\033[0m')
if __name__=='__main__':
    print(login())
