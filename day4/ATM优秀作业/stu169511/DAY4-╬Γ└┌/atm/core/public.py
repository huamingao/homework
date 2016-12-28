import json,os,sys
base_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
db_path = base_dir + os.path.sep + 'db'+ os.path.sep#db目录的绝对路径
log_path = base_dir + os.path.sep + 'log'+ os.path.sep#log目录的绝对路径
def op_file(path):
    f = open(path,'a+')
    f.seek(0)
    dic = json.load(f)
    return dic
def get_username():#取用户名
    with open(db_path + 'user_status.txt') as f:
        user = f.read()
    return user
def write_atm_log(func):#记录atm操作日志
    f1 = open(log_path + 'atm.log','w')
    f1.write(func)
    f1.flush()
    f1.close()
    return True
def write_access_log(func):#记录atm操作日志
    f1 = op_file(log_path + 'access.log')
    f1.write(func)
    f1.flush()
    f1.close()
    return True