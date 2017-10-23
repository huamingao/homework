#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from core.client import FTPClient

HOST,PORT = 'localhost',5555



if __name__ == '__main__':
    client = FTPClient()
    client.connect((HOST,PORT))
    client.interactive()