#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES_DIR = os.path.join(PROJECT_DIR,'db','courses')


class Course:

    def __init__(self,name,time,fee,teacher_obj):
        self.name = name
        self.time = time
        self.fee = fee
        self.teacher_obj = teacher_obj
        self.file = os.path.join(COURSES_DIR,name)

