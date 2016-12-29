#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


from src.user import User


TYPE = '女神'
SEX = '女'


class Girl(User):

    type = TYPE
    sex = SEX

    def __init__(self,name,password='',age=19,money=3000):
        self.name = name
        self.password = password
        self.age = age
        self.money = money