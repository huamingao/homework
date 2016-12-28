#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import re


from src import bracket as src_bracket
from src import compute as src_compute
from src import validate as src_validate


INPUT_INVALID = '您输入的表达式有误，请重新输入！'


def remove_bracket(expression):
    """
    递归函数，从最内层带括号的表达式开始计算，调用compute函数获得括号内表达式计算结果，
    拼接成新的表达式，将新表达式传入本函数入口进行递归调用，直到表达式中不存在括号，再调用compute进行纯粹的加减乘除运算
    :param expression:
    :return:
    """
    # 递归出口。如果表达式中已经没有括号，返回这个不带括号的表达式
    if not re.findall('^.*\(.*\).*$', expression):
        return expression
    else:
        # 获取当前最内层括号中的字符
        # [\+\-\*\/]?\d+\.*\d* 匹这些字符：整数、小数、前面带一个加减乘除号的整数或小数
        content = re.search('\(([\+\-\*\/]*\d+\.?\d*)+\)',expression).group()
        # 去掉content中的括号
        content = content[1:len(content)-1]
        # 下面一行用于测试
        #print('当前表达式的最内层括号里的内容：',content)

        # 如果content是正数字符，自动补齐使其符合表达式格式，例如，5 补齐为 0+5
        if re.match('^\d+\.?\d*$',content):
            content = '%s%s' %('0+',content)
            # 下面一行用于测试
            #print('自动补齐之后:', content)
        # 如果content是负数字符，自动补齐使其符合表达式格式，例如，-5 补齐为 0-5
        if re.match('^\-\d+\.?\d*$',content):
            content = '%s%s' %('0',content)
            # 下面一行用于测试
            #print('自动补齐之后:',content)
        # 如果content是表达式
        else:
            # 调用compute函数计算表达式
            result = src_compute.compute(content)

        # 以当前最内层括号为界，将当前表达式分割为3部分
        head = re.split('\(([\+\-\*\/]*\d+\.?\d*)+\)',expression,1)[0]
        tail = re.split('\(([\+\-\*\/]*\d+\.?\d*)+\)',expression,1)[-1]

        # 拼接成新的表达式
        seq = (head,result,tail)
        expression = ''.join(seq)
        return remove_bracket(expression)


