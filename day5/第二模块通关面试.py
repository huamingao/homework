#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

# 编程题
# 已知有list_a = ['b','A','c','D']，对其进行排序，返回结果是如下顺序['A','b','c','D']

# 方法一
print(sorted(['b','A','c','D'], key = lambda x : x.upper()))

# print(dir(1))
# 方法二
def mysorted(list_a):
    tmp_dict = {}
    for l in list_a:
        tmp_dict[l.upper()] = l
    tmp_list = tmp_dict.keys()
    tmp_list = sorted(tmp_list)
    res_list = []
    for l in tmp_list:
        res_list.append(tmp_dict[l])
    return res_list
print(mysorted(['b','A','c','D']))


# 方法三：
list_a = ['b','A','c','D']
upper_list_a = []
sorted_list_a = []
# ['A','b','c','D']

for i in list_a:
    upper_list_a.append(i.upper())
    upper_list_a.sort()

for i in upper_list_a:
    if i in list_a:
        sorted_list_a.append(i)
    else:
        sorted_list_a.append(i.lower())

print(sorted_list_a)


