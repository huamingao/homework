#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os, sys,socketserver,json,hashlib,socket,pickle
from conf.setting import USERS,DATA_DIR

class MyTCPHandler(socketserver.BaseRequestHandler):

    def get_tree_size(path):
        """Return total size of files in given path and subdirs."""
        total = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                total += MyTCPHandler.get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
        return total

    def cd(self,**kwargs):
        # remain in current directory
        if kwargs['directory'] == '.':
            abs_directory = os.path.join(DATA_DIR, kwargs['current_dir'])
        # change to parent directory
        elif kwargs['directory'] == '..':
            abs_directory = os.path.dirname(os.path.join(DATA_DIR, kwargs['current_dir']))
        # change to user home directory
        elif kwargs['directory'] == '~':
            abs_directory = os.path.join(DATA_DIR, kwargs['username'])
        # change to sub directory
        else:
            abs_directory = os.path.join(DATA_DIR,kwargs['current_dir'],kwargs['directory'])
        if not os.path.isdir(abs_directory):
            print('{} directory not found on server'.format(abs_directory))
            self.request.send(b'directory not found')
        else:
            self.request.send(b'directory changed')

    def list(self,**kwargs):
        """
        list files in current directory
        :param kwargs:
        :return:
        """
        if kwargs['directory'] == '.':
            abs_directory = os.path.join(DATA_DIR, kwargs['current_dir'])
        else:
            abs_directory = os.path.join(DATA_DIR,kwargs['current_dir'],kwargs['directory'])
        if not os.path.isdir(abs_directory):
            print('{} directory not found on server'.format(abs_directory))
            self.request.send(b'directory not found')
        else:
            self.request.send(json.dumps(os.listdir(abs_directory)).encode())

    def put(self,**kwargs):
        """
        receive file from client
        :return:
        """
        filename = kwargs['filename']
        client_file_size = kwargs['size']
        abs_filename = os.path.join(DATA_DIR, kwargs['current_dir'], filename)
        # check whether the user quota is enough for the file to be uploaded
        with open(os.path.join(USERS, kwargs['username']), 'rb') as f:
            user = pickle.load(f)
        # if quota is not enough, send msg 'quota limit'
        if user.quota < client_file_size + MyTCPHandler.get_tree_size(os.path.join(DATA_DIR,user.username)):
            self.request.send('quota limit {}'.format(int(user.quota/1024/1024)).encode())
            return None
        # if the file does not exist on server, set sending msg to '0'
        elif not os.path.isfile(abs_filename):
            received_size = 0
            self.request.send(str(received_size).encode())
        # if the file already exists on server, set sending msg to the number of actual file size
        else:
            received_size = os.stat(abs_filename).st_size
            self.request.send(str(received_size).encode())
        recv = self.request.recv(1024)
        if  recv == 'override'.encode():
            os.remove(abs_filename)
            self.request.send('ok'.encode())
            received_size = 0
        elif recv == 'ready'.encode():
            self.request.send('ok'.encode())
        # receive file per 1024
        server_md5 = hashlib.md5()
        with open(abs_filename,'ab') as f:
            f.seek(received_size)
            print('client upload from ', received_size)
            while received_size < client_file_size:
                data = self.request.recv(1024)
                f.write(data)
                server_md5.update(data)
                received_size += len(data)sho
            else:
                self.request.send(server_md5.hexdigest().encode())
                if self.request.recv(1024) == b'uploaded':
                    print('{} uploaded successfully'.format(filename))

    def get(self,**kwargs):
        """
        send file(s) to client
        :param kwargs:
        :return:
        """
        filename = kwargs['filename']
        abs_filename = os.path.join(DATA_DIR,kwargs['current_dir'],filename)
        if not os.path.isfile(abs_filename):
            self.request.send(b'not exist')
            print('{} does not exist on server'.format(filename))
        else:
            # send the filename and size
            msg_dic = {
                'current_dir': kwargs['current_dir'],
                'filename': filename,
                'total_size': os.stat(abs_filename).st_size
            }
            self.request.send(json.dumps(msg_dic).encode())
            # receive "action cancelled" or "override" or "continue download" from client
            client_resp = self.request.recv(1024)
            if client_resp == b'action cancelled':
                print('client cancel download')
                return None
            elif client_resp == b'override':
                kwargs['received_size'] = 0
            elif client_resp == b'read to receive':
                pass
            server_md5 = hashlib.md5()
            with open(abs_filename,'rb') as f:
                f.seek(kwargs['received_size'])
                print('client download from ',kwargs['received_size'])
                for line in f:
                    self.request.send(line)
                    server_md5.update(line)
            client_md5 = self.request.recv(1024).decode()
            if client_md5 == server_md5.hexdigest():
                self.request.send(b'downloaded')
                print('{} downloaded successfully'.format(filename))

    def logon(self,**kwargs):
        username,recv_password = kwargs['username'],kwargs['password']
        if not os.path.isfile(os.path.join(USERS,username)):
            msg_dic = {
                'username': username,
                'authenticated': 'NoExist'
            }
        else:
            with open(os.path.join(USERS,username),'rb') as f:
                user = pickle.load(f)
            if recv_password != user.password:
                msg_dic = {
                    'username':username,
                    'authenticated':False
                }
            else:
                msg_dic = {
                    'username':username,
                    'server_dir':user.server_dir,
                    'authenticated':True
                }
                print('{} logon'.format(username))
        self.request.send(json.dumps(msg_dic).encode())

    def register(self,**kwargs):
        username, recv_password, quota = kwargs['username'], kwargs['password'],kwargs['user_quota']
        pwd_hash = hashlib.md5()
        pwd_hash.update(b'')
        if os.path.isfile(os.path.join(USERS,username)):
            msg_dic = {
                'username': username,
                'authenticated': 'AlreadyExist'
            }
        elif recv_password == pwd_hash.hexdigest():
            msg_dic = {
                'username':username,
                'authenticated': 'StopRegister'
            }
        else:
            user = User(username,recv_password,quota)
            with open(os.path.join(USERS,username),'wb') as f:
                pickle.dump(user,f)
            os.mkdir(user.server_dir)
            msg_dic = {
                'username':username,
                'authenticated':'registered'
            }
            print('{} registered'.format(username))
        self.request.send(json.dumps(msg_dic).encode('utf-8'))

    @staticmethod
    def logoff(**kwargs):
        print('{} logoff'.format(kwargs['username']))

    @staticmethod
    def exit(**kwargs):
        print('{} exit. client closed'.format(kwargs['username']))

    def handle(self):
        """
        :return:
        """
        while True:
            try:
                # self.request is the TCP socket connected to the client
                print('{} writing:'.format(self.client_address[0]))
                data_dict = json.loads(self.request.recv(1024).strip().decode())
                action = data_dict['action']
                # return whether the object has an attribute with the given name
                if hasattr(self, action):
                    # get a named attribute from an object
                    func = getattr(self, action)
                    # **的作用是解包字典，这里用到了反射
                    func(**data_dict)
                else:
                    print('{}:action not found'.format(action))
            except ConnectionResetError as e:
                print('err:',e)
                break


class User(MyTCPHandler):

    def __init__(self,username,password,quota):
        self.username = username
        self.password = password
        self.quota = quota
        self.server_dir = os.path.join(DATA_DIR,username)