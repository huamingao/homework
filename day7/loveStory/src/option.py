#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


QUIZ_INFO = '''
问题：{0}
A. {1}
B. {2}
C. {3}
D. {4}
'''


class Quiz(object):

    def __init__(self,phase,question,optA,optB,optC,optD):
        # 问题对应的人生阶段：学生、职场新人、职场达人
        self.phase = phase
        self.question = question
        self.optA = optA
        self.optB = optB
        self.optC = optC
        self.optD = optD

    def show(self):
        print(QUIZ_INFO.format(self.question,self.optA,self.optB,self.optC,self.optD))





quiz1 = Quiz('学生','刚进大学，你决定选修下面哪个课程？','计算机科学','金融学','吉他','文学')

