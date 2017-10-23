#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)
SERVER_ADDR = ('localhost', 6969)


from src.server import *


if __name__ == '__main__':
    print(PROJECT_DIR)
    server_socket()