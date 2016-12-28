#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:yangjian

menu = {"河北省":{"石家庄市":['平山县','无极县','灵寿县'],"衡水市":['饶阳县','安平县','武强县'],},
            "山东省":{"济南市":['济阳县','商河县','平阴县'],"青岛市":['市南区','市北区','市东区'],},
            "河南省":{"洛阳市":['新安县','洛宁县','宜阳县'],"郑州市":['金水区','惠济区','上街区'],}}

exit_flag = False
while not exit_flag:
    for index,key in enumerate(menu.keys()):
        print(index,key)
    choice_1 = input("请选择省份:").strip()
    if choice_1.isdigit():
        choice_1 = int(choice_1)
        key_1 = list(menu.keys())[choice_1]
        while not exit_flag:
            for index,key in enumerate(menu[key_1]):
                print("-->",index,key)
            choice_2 = input("请选择城市:").strip()
            if choice_2.isdigit():
                choice_2 = int(choice_2)
            key_2 = list(menu[key_1].keys())[choice_2]
            while not exit_flag:
                for index,key in enumerate(menu[key_1][key_2]):
                    print("-->-->",index,key)
                choice_3 =  input("最后一级菜单，如果要回退上一级请输入'b',退出输入'q':")
                if choice_3 == 'q':
                    exit_flag = True
                elif choice_3 == 'b':
                    break

else:
     print("----------再见 ---------------")
