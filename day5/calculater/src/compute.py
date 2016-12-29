#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import re


from src import bracket as src_bracket
from src import validate as src_validate


def compute(expression):
    """
    递归进行乘除。先计算第一个运算数与第二个运算数，再计算该结果与第三个运算数，得到结果后再与第四个运算符操作，依次类推
    :return:
    """
    # 递归出口，如果表达式中没有乘除号，调用compute_add_sub函数计算所有加减法
    if not re.findall('[\*\/]',expression):
        # 下面一行用于测试
        #print('结束了所有乘除法，获得表达式：',expression)
        result = compute_add_sub(expression)
        return result
    else:
        # 获取最基本乘除法表达式
        # 定位第1个乘除号为界，将表达式分割为5部分，形成列表，第1个元素是乘除法第1个运算数以前的所有字符，第2个元素是第1个运算数，
        # 第3个元素是第1个运算符，第4个元素是第2个运算数，第5个元素是剩下的表达式（进入下一轮递归）
        head, num1, operator, num2, tail = re.search('(.*)(\d+\.?\d*)([\*\/])(\d+\.?\d*)(.*)',expression).groups()
        # 根据操作符，对取出的运算数进行计算
        if operator == '*':
            result = float(num1) * float(num2)
        elif operator == '/':
            result = float(num1) / float(num2)
        # 将计算结果转为字符，拼接为新的表达式，以便进入下一轮递归
        seq = (head,str(result),tail)
        expression = ''.join(seq)
        return compute(expression)


def compute_add_sub(expression):
    """
    递归进行加减。先计算第1个运算数与第2个运算数，再计算该结果与第3个运算数，得到结果后再与第4个运算符操作，依次类推
    :param expression:
    :return:
    """
    # 递归出口，计算完毕所有的加减号，返回结果
    if re.match('^\-?\d+\.?\d*$',expression):
        # 下面一行用于测试
        #print('结束了所有加减法，获得数字字符',expression)
        return expression
    # 如果表达式中尚有加减号，找到第一个加减号，计算，递归调用这段代码，直到消除所有的加减号
    else:
        # 以第1个运算符为界，将表达式分割为4部分，形成列表，第1个元素是第1个运算数，第2个元素是第1个运算符，
        # 第3个元素是第2个运算数，第4个元素是剩下的表达式（进入下一轮递归）
        num1,operator,num2,tail = re.search('(\-?\d+\.?\d*)([\+\-])(\-?\d+\.?\d*)(.*)',expression).groups()
        # 根据操作符，对最后两个数字字符进行计算
        if operator == '+':
            result = float(num1) + float(num2)
        elif operator == '-':
            result = float(num1) - float(num2)
        # 将计算结果转为字符，拼接为新的表达式，以便进入下一轮递归
        seq = (str(result),tail)
        expression = ''.join(seq)
        return compute_add_sub(expression)


