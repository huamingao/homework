#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

import socketserver
from core.server import MyTCPHandler
from conf.setting import HOST,PORT

# HOST,PORT = 'localhost',5555

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    print('start listening...')
    # server_forever方法：handle requests until an explicit shutdown() request
    server.serve_forever()