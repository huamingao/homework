#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import socket,hashlib,os,json,sys,time,re
from conf.setting import PROJECT_DIR,CLIENT_DIR


MSG = '''
============
Instructions
============
list <directory>   -- list items in the directory. list items in current directory if no directory is specified
cd <directory>     -- change directory to. ~ means home directory, . means current directory, .. means parent directory
get <filename>     -- download file from server
put <filename>     -- upload file to server
logoff             -- logoff current user
exit               -- close client
help               -- show these instructions
'''


class FTPClient(object):

    def __init__(self):
        self.client = socket.socket()
        self.user = User(self.client)

    @staticmethod
    def help():
        print(MSG)

    def connect(self,addr):
        """
        连接服务器，引导用户登录/注册
        :param addr:
        :return:
        """
        self.client.connect(addr)
        if not self.user.authenticated:
            res = self.user.logon()
            if res == 'exit':
                exit()
        else:
            print('{0}, you have already logon'.format(self.user.username))

    def cd(self,*args):
        directory = ' '.join(args)
        directory = directory.strip('"').strip('\'')
        print(directory)
        if directory == '..' and self.user.current_dir == self.user.username:
            print('no permission to go out of your home directory')
            return None
        msg_dic = {
            'action':'cd',
            'username':self.user.username,
            'current_dir':self.user.current_dir,
            'directory': directory
        }
        self.client.send(json.dumps(msg_dic).encode())
        server_resp = self.client.recv(1024)
        if server_resp == b'directory not found':
            print('the directory {} does not exist on server'.format(args[0]))
        elif server_resp == b'directory changed':
            # remain in current directory
            if directory == '.':
                pass
            # change to user home directory
            elif directory == '~':
                self.user.current_dir = self.user.username
            # change to parent directory
            elif directory == '..':
                self.user.current_dir = os.path.dirname(self.user.current_dir)
            # change to sub directory
            else:
                self.user.current_dir = '\\'.join((self.user.current_dir,directory))
            print('has changed to the directory {}'.format(self.user.current_dir))

    def list(self, *args):
        """
        list files
        :return:
        """
        directory = ' '.join(args)
        directory = directory.strip('"').strip('\'')
        if directory == '..' and self.user.current_dir == self.user.username:
            print('no permission to list items out of your home directory')
            return None
        msg_dic = {
            'action':'list',
            'current_dir':self.user.current_dir,
            'directory': directory
        }
        self.client.send(json.dumps(msg_dic).encode())
        server_resp = self.client.recv(1024)
        if server_resp == b'directory not found':
            print('the directory {} does not exist'.format(directory))
        elif server_resp.decode() == '[]':
            print('the directory is empty')
        else:
            # print file name one by one
            for file in json.loads(server_resp.decode()):
                print(file)

    @staticmethod
    def progressbar(size,operated_size):
        """
        显示进度条
        :param total:
        :return:
        """
        # 已传输数据占总大小的百分比
        percentage = int(operated_size / size * 100)
        # 每当已传输数据达到数据总量的下一个整倍数，更新一次进度条
        if ( percentage - 1) in range(100):
            num = int(percentage / 10 * 5 ) + 1
            # /r 转义符，表示回到行首
            r = ' \r %s>%d%%' % ('=' * num, percentage,)
            sys.stdout.write(r)
            sys.stdout.flush()
        else:
            pass

    def put(self, *args):
        """
        upload file(s) to server
        :param args:
        :return:
        """
        for filename in args:
            abs_filename = os.path.join(CLIENT_DIR, self.user.current_dir, filename)
            # if the file does not exist on client
            if not os.path.isfile(abs_filename):
                print(filename, ' does not exist on client')
            # if the file exists on client
            else:
                size = os.stat(abs_filename).st_size
                msg_dic = {
                    'action': 'put',
                    'username': self.user.username,
                    'current_dir':self.user.current_dir,
                    'filename': filename,
                    'size': size
                }
                self.client.send(json.dumps(msg_dic).encode())
                # receive server ACK
                server_resp = self.client.recv(1024)
                # if 'quota limit' received
                if server_resp.decode().startswith('quota limit'):
                    print('Your {}MB, not enough for the file to be uploaded'.format(server_resp.decode()))
                    continue
                # if digit number received, means the file already exists on server
                else:
                    server_file_size = int(server_resp.decode())
                    # if file size is the same as the file on client
                    if server_file_size == os.stat(abs_filename).st_size:
                        option = input('{} already exist on server. Override? y/n:'.format(filename))
                        # if refuse to override the existed file, cancel upload
                        if option != 'y':
                            print('upload cancelled for {}'.format(filename))
                            continue
                        # to continue override, set size=0
                        else:
                            server_file_size = 0
                            self.client.send('override'.encode())
                            self.client.recv(1024)
                    # if file size is not smaller than the file on client, continue previous download
                    elif 0 < server_file_size < os.stat(abs_filename).st_size:
                        option = input('Continue to download the file {}? y/n:'.format(filename))
                        if option != 'y':
                            self.client.send(b'action cancelled')
                            print('download cancelled for {}'.format(filename))
                            continue
                        else:
                            self.client.send('ready'.encode())
                            self.client.recv(1024)
                    else:
                        self.client.send('ready'.encode())
                        self.client.recv(1024)
                # start to send file content line by line
                client_md5 = hashlib.md5()
                print('{} is uploading,please wait:'.format(filename))
                with open(abs_filename, 'rb') as f:
                    print('client upload from ',server_file_size)
                    f.seek(server_file_size)
                    for line in f:
                        self.client.send(line)
                        client_md5.update(line)
                        server_file_size += len(line)
                        FTPClient.progressbar(msg_dic['size'], server_file_size)
                server_md5 = self.client.recv(1024)
                if server_md5.decode() == client_md5.hexdigest():
                    self.client.send(b'uploaded')
                    print('\n{} uploaded successfully'.format(filename))

    def get(self, *args):
        """
        download file(s) from server
        :return:
        """
        for filename in args:
            abs_filename = os.path.join(CLIENT_DIR,self.user.current_dir,filename)
            # if file already exist on client
            if os.path.isfile(abs_filename):
                client_msg_dic = {
                    'action': 'get',
                    'username': self.user.username,
                    'current_dir':self.user.current_dir,
                    'filename': filename,
                    'received_size':os.stat(abs_filename).st_size
                }
            # if file not exist on client, set transfer_size to 0
            else:
                client_msg_dic = {
                    'action': 'get',
                    'username': self.user.username,
                    'current_dir':self.user.current_dir,
                    'filename': filename,
                    'received_size':0
                }
            self.client.send(json.dumps(client_msg_dic).encode())
            server_resp = self.client.recv(1024)
            if server_resp == b'not exist':
                print('{} does not exist on server'.format(filename))
                continue
            else:
                server_msg_dic = json.loads(server_resp.decode())
            # if file exists on client, and refuse to continue download
            if server_msg_dic['total_size'] > client_msg_dic['received_size'] > 0:
                option = input('Continue to download the file {}? y/n:'.format(filename))
                if option != 'y':
                    self.client.send(b'action cancelled')
                    print('download cancelled for {}'.format(filename))
                    continue
                else:
                    self.client.send(b'read to receive')
            # if file exists on client, and refuse to override
            elif server_msg_dic['total_size'] == client_msg_dic['received_size']:
                option = input('{} already exist on client. override? y/n:'.format(filename))
                if option != 'y':
                    self.client.send(b'action cancelled')
                    print('download cancelled for {}'.format(filename))
                    continue
                else:
                    self.client.send(b'override')
                    os.remove(abs_filename)
                    client_msg_dic['received_size'] = 0
            else:
                self.client.send(b'read to receive')
            # start to download file content
            client_md5 = hashlib.md5()
            print('{} is writing,please wait:'.format(filename))
            # download file content per 1024
            try:
                with open(abs_filename,'ab') as f:
                    print('client download from ', client_msg_dic['received_size'])
                    f.seek(client_msg_dic['received_size'])
                    while client_msg_dic['received_size'] < server_msg_dic['total_size']:
                        data = self.client.recv(1024)
                        f.write(data)
                        client_msg_dic['received_size'] += len(data)
                        client_md5.update(data)
                        FTPClient.progressbar(server_msg_dic['total_size'], client_msg_dic['received_size'])
                    else:
                        self.client.send(client_md5.hexdigest().encode())
                        if self.client.recv(1024) == b'downloaded':
                            print('\n{} downloaded successfully'.format(filename))
            except KeyboardInterrupt:
                 print('You pressed Ctrl-C. Download interrupt')

    def logoff(self):
        self.user.logoff()
        self.user.logon()

    def exit(self):
        # 终止客户端程序
        msg_dic = {
            'action':'exit',
            'username':self.user.username
        }
        self.client.send(json.dumps(msg_dic).encode())
        self.user.authenticated = False
        self.client.close()
        print('{} logoff. client closed'.format(self.user.username))
        exit()

    def interactive(self):
        """
        根据用户输入的命令，跳转到相应的类方法，利用了反射
        :return:
        """
        while True:
            cmd = input('{}>>:'.format(self.user.current_dir))
            if len(cmd) == 0:continue
            action = cmd.split()[0]
            content = tuple(cmd.split()[1:])
            # return whether the object has an attribute with the given name
            if hasattr(self,action):
                # get a named attribute from an object
                func = getattr(self,action)
                # content is a list, *的作用是解包列表
                # 这里用到了反射
                func(*content)
            else:
                FTPClient.help()


class User(object):

    def __init__(self,socket_obj,username=None,quota=524288000):
        # 初始化User对象
        self.username = username
        self.current_dir = None
        self.quota = quota
        self.authenticated = False
        self.client = socket_obj

    def register(self):
        # 用户注册
        while True:
            username = input('register username:')
            if username == '':
                print('Registeration cancelled')
                break
            else:
                # getpass is only for linux platform
                # password = getpass.getpass(SET_PWD.format(name))
                # for windows platform
                password = input('register password:')
                # 用户密码经md5加密后传送
                password_hash = hashlib.md5()
                password_hash.update(password.encode())
                # set quota
                quota = input('set your quota in MB(skip it by clicking enter): ')
                if quota == '':
                    quota == None
                else:
                    quota = int(quota) * 1024 * 1024
                msg_dic = {
                    'action':'register',
                    'username':username,
                    'password':password_hash.hexdigest(),
                    'user_quota':quota
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                res_dic = json.loads(self.client.recv(1024).decode())
                if res_dic['authenticated'] == 'AlreadyExist':
                    print('user already exists,click enter to exit registeration')
                elif res_dic['authenticated'] == 'StopRegister':
                    print('Registeration cancelled')
                    break
                elif res_dic['authenticated'] == 'registered':
                    os.mkdir(os.path.join(CLIENT_DIR,username))
                    print('successfully registered')
                    break

    def logon(self):
        # 用户登录
        while True:
            option = input('1. login\n2. register as new user\nplease input your option: ')
            if option == 'exit':
                return 'exit'
            elif option not in ['1','2']:
                print('wrong input, please try again. input exit to close the program')
            elif option == '2':
                self.register()
            elif option == '1':
                username = input("username：").strip()
                if len(username) == 0:continue
                else:
                    password = input("password：").strip()
                    # 用户密码经md5加密后传送
                    password_hash = hashlib.md5()
                    password_hash.update(password.encode())
                    msg_dic = {
                        'action':'logon',
                        'username':username,
                        'password':password_hash.hexdigest()
                    }
                    self.client.send(json.dumps(msg_dic).encode())
                    res_dic = json.loads(self.client.recv(1024).decode())
                    if res_dic['username'] == username:
                        # 密码错误
                        if not res_dic['authenticated']:
                            print("authentication fails, please try again！")
                        # 用户不存在
                        elif res_dic['authenticated'] == 'NoExist':
                            option = input('username not exist, register? y/n: ')
                            if option == 'y':
                                self.register()
                            else:
                                continue
                        # 登录成功
                        elif res_dic['authenticated']:
                            print("{0}, you have successfully logon！".format(res_dic['username']))
                            print(MSG)
                            self.username = res_dic['username']
                            self.authenticated = True
                            self.current_dir = self.username
                            break

    def logoff(self):
        # 用户退出登录（客户端程序仍运行）
        msg_dic = {
            'action':'logoff',
            'username':self.username
        }
        self.client.send(json.dumps(msg_dic).encode())
        self.authenticated = False



