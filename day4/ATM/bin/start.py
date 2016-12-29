#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from src import crontab as src_crontab


if __name__ == "__main__":
    src_crontab.main()
