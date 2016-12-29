#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao


import re

from src import bracket as src_bracket
from src import compute as src_compute
from src import validate as src_validate


INPUT_INVALID = '您的输入有误！请重新输入'
INVALID_OPERATOR = '您输入的运算符有误！请重新输入'
INVALID_BRAKET = '您输入的括号不成对！请重新输入'


def validate(expression):
    """
    判断表达式是否合法
    :return:
    """
    # [\d\+\-\*\/\(\)] 字符组，包括加减乘除号、括号、数字字符
    # [^\d\+\-\*\/\(\)] 对上述字符组取反，匹配所有不在上述字符组中的字符，如果找到，提示输入表达式有非法字符，返回False
    if re.findall('[^\d\+\-\*\/\(\)\.]',expression):
        print(INPUT_INVALID)
        return False

    # 如果匹配到连续的加减乘除号，提示输入有误，返回False
    elif re.findall('[\+\-\*\/\.]{2,}',expression):
        print(INVALID_OPERATOR)
        return False

    # 如果表达式中包含括号
    elif re.findall('[\(\)]',expression):
        # 定义模式，用于匹配配对的括号
        pattern = '[^\(\)]*\([^\(\)]+\)[^\(\)]*'
        # 循环匹配，只要匹配到配对的括号，就将它们替换为占位符’0‘
        while re.findall(pattern,expression):
            expression = re.sub(pattern,'0',expression)
        else:
            # 循环匹配结束后，如果不存在括号，说明表达式中括号全部正确配对，用户输入无误，因此返回True
            if not re.findall('[\(\)]+',expression):
                return True
            # 如果还存在正括号或反括号，说明是无法配对的单一括号，说明用户输入的表达式有误，返回False
            else:
                print(INVALID_BRAKET)
                return False
    else:
        return True


