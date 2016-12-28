#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import re
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from src import bracket as src_bracket
from src import compute as src_compute
from src import validate as src_validate


INPUT_EXPRESSION = '请输入要计算的表达式，退出程序请输q：'
RESULT = '计算结果：{0}'

# 使用 __name__ 的目的：
#   只有执行 python index.py 时，以下代码才执行
#   如果其他人导入该模块，以下代码不执行

if __name__ == "__main__":
    expression = ''
    while expression != 'q':
        expression = input(INPUT_EXPRESSION)
        if expression == 'q':
            exit()
        else:
            # 如果输入的表达式合法
            if src_validate.validate(expression):
                # 调用remove_bracket函数去除所有括号,重新赋值给expression
                # 下面一行用于测试
                expression = src_bracket.remove_bracket(expression)
                #print('去掉了全部括号！当前表达式为：',expression)
                # 调用compute函数进行加减乘除运算
                result = src_compute.compute(expression)
                # 如果result是小数且小数点后字符为0，就去掉小数点及其之后的字符，即按整型打印
                result = re.sub('\.0','',result)
                print(RESULT.format(result))