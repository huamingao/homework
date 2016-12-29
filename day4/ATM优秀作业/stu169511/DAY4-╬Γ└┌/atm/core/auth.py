import json,sys,os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#当前文件的父级-父级目录--atm目录的绝对路径
sys.path.append(base_dir)
db_path = base_dir + os.path.sep + 'db'+ os.path.sep#db目录的绝对路径
from core import public
from core import login
USER_JSON = base_dir + os.path.sep + 'db' + os.path.sep + 'user.json'
def auth(func):
    '''
    登录状态校验装饰器
    :param func:
    :return:
    '''
    def wrapper(*args,**kwargs):
        f = open(db_path + 'user_status.txt','r')
        content = f.readlines()
        try:
            if len(content)>0:
                res = func(*args,**kwargs)
                return res
        except Exception:
            print('\033[1;31;0m未登录，请登录！\033[0m')
            login.login()
        func(*args,**kwargs)
    return wrapper