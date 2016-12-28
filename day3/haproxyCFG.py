#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao
'''
问题
1、删除时有bug
请输入要删除的记录：
{"backend":"buy.oldboy.org","record":{"server":"100.1.7.90","weight":20,"maxconn":3000}}
您要删除的内容不存在
退出整个程序请输q,继续操作请输非q的任意键
这条记录应该是存在的
本程序可以对HAproxy配置文件进行如下操作。退出程序请输q
1 查看
2 添加
3 修改
4 删除
5 备份

如要进行操作，请输入相应的编号：1
请输入要查询的backend：buy.oldboy.org
backend buy.oldboy.org的记录如下：
server 100.1.7.90 100.1.7.90 weight 20 maxconn 3000

而且删除应该只需要backend以及record的server信息就够了
请输入要删除的记录：
{"backend":"buy.oldboy.org","record":{"server":"100.1.7.90"}}
您的输入不合法！

总的来说一如既往的好，good，继续保持
'''
import os
import json

# 全局变量
FILE = 'haproxy.cfg'
FILE_BAK = 'haproxy.cfg_bak'

RULE_MSG = '''
本程序可以对HAproxy配置文件进行如下操作。退出程序请输q
1 查看
2 添加
3 修改
4 删除
5 备份
'''
INVALID_MSG = '\033[31;1m您的输入不合法！\033[0m'
NO_FILE_MSG = '\033[31;1mhaproxy配置文件不存在，请重定向到正确的目录\033[0m'
RECORD_MSG = 'backend {0}的记录如下：'
NO_BACKEND_MSG = '\033[31;1m您所输入的backend不存在\033[0m'
FAIL_DELETE_MSG = '\033[31;1m您要删除的内容不存在\033[0m'
BACKEND_EXIST_MSG = '\033[31;1m您所输入的backend已存在！\033[0m'
CONTENT_MSG = '''
请按如下格式输入，一次只能输入一条记录
{"backend":"www.oldboy.org","record":{"server":"100.1.8.9","weight":20,"maxconn":30}}
'''
SUCCESS_MSG = '''
您输入的内容已成功{0}如下
backend {1}
        {2}
'''
DUPLICATE_CONTENT_MSG = '您输入的内容已经存在于配置文件中了!'
BAK_MSG = '当前haproxy.cfg已备份到haproxy.cfg_bak'
ADD_RECORD_MSG = '您输入的IP不存在，已将其添加为指定backend的一条新增记录'

OPTION_PROMPT = '如要进行操作，请输入相应的编号：'
BACKEND_PROMPT = '请输入要{0}的backend：'
RECORD_PROMPT = '请输入要{0}的记录：\n'
CONTINUE_PROMPT = '\033[31;1m退出整个程序请输q,继续操作请输非q的任意键\033[0m'

CHECK_MSG = '查询'
ADD_MSG = '添加'
MODIFY_MSG = '修改'
DELETE_MSG = '删除'

def check(backend):
    """
    用户输入1时调用
    :return: None
    """
    flag = 0
    serverList = []
    # 如果haproxy文件不存在，提示文件不存在
    if not os.path.exists(FILE):
        print(NO_FILE_MSG)
    # 如果文件存在
    else:
        seq = ('backend',backend)
        backend_line = ' '.join(seq)
        with open(FILE,'r',encoding='utf-8') as f:
            for line in f:
                # 逐行遍历文件，如果发现指定行，flag置为1，进入下一行
                if line.strip() == backend_line:
                    flag = 1
                    continue
                # 如果下一行以backend打头，说明不是要获取的行，flag置为0，结束循环
                if flag == 1 and line.strip().startswith('backend'):
                    flag = 0
                    break
                # 如果flag为1，且该行不为空，说明是要获取的行，将该行追加到列表serverList
                if flag == 1 and line.strip() != '':
                    serverList.append(line.strip())
    return serverList


def trans_content(content):
    """
    用于将输入的内容转化为字典，获取backend，和record行
    :param content: 传入输入的内容
    :return: backend, record
    """
    try:
        # 字符串转换为字典
        content_dic = json.loads(content)
        # 从字典中获取backend,server,weight,maxconn
        backend = content_dic['backend']
        server = content_dic['record']['server']
        weight = str(content_dic['record']['weight'])
        maxconn = str(content_dic['record']['maxconn'])
        # 构造record行
        seq = ('server',server,'weight',weight,'maxconn',maxconn)
        record = ' '.join(seq)
        return backend,record
    except:
        return None


def add(backend,record):
    """
    用户输入2时调用，添加backend和记录
    :param backend: 域名
    :param record: 记录
    :return: True 添加成功 False 要添加的内容已存在
    """
    # 调用backup函数得到配置文件的备份文件
    backup()
    # 调用check函数，如果backend已经存在于文件中，就将现有的backend记录返回
    serverList = check(backend)
    with open(FILE_BAK, 'r', encoding='utf-8') as f_bak, open(FILE, 'w', encoding='utf-8') as f:
        # 如果serverList为空，说明backend不存在
        if not serverList:
            # 从备份文件往原配置文件覆盖写，在文件末尾追加新增的backend和record行
            for line in f_bak:
                f.write(line)
            f.write('\n'*2 + 'backend ' + backend + '\n')
            f.write( ' ' * 8 + record + '\n')
            return True
        # 如果serverList不为空，说明backend存在
        else:
            # 如果要新增的record已经存在于serverList中，说明要新增的backend和record行都已经存在在原配置文件中了，直接返回False
            if record in serverList:
                return False
            # 如果要新增的record不在serverList，从备份文件往原配置文件覆盖写，其中，在定位到backend行时，在其下新增写入record行
            else:
                for line in f_bak:
                    f.write(line)
                    # 如果backend已经存在于haproxy配置文件中
                    if line.strip() == 'backend ' + backend:
                        f.write(' ' * 8 + record + '\n')
                        continue
                return True


def modify(backend,record):
    """
    用户输入3时调用，修改指定backend的记录
    :return: True 修改成功 False 要修改的backend不存在
    """
    # 从content中获取backend，server
    # 调用backup函数得到配置文件的备份文件
    backup()
    # 调用check函数，如果backend已经存在于文件中，就将其下记录返回
    serverList = check(backend)
    # 如果serverList为空，说明backend不存在，调用add函数添加这个backend和record行
    if not serverList:
        add(backend, record)
        return True
    # 如果serverList不为空，说明backend存在
    else:
        flag = 0
        # 如果要输入的record已经存在于serverList中，说明没有要修改的内容，直接返回False
        if record in serverList:
            return False
        # 如果要输入的record不在serverList
        else:
            with open(FILE_BAK, 'r', encoding='utf-8') as f_bak, open(FILE, 'w', encoding='utf-8') as f:
                # 从备份文件往原配置文件覆盖写
                for line in f_bak:
                    # 遇到指定backend的记录集时
                    if line.strip() in serverList:
                        # 判断record中的IP是否存在于当前行中，若是，在当前位置添加record行，跳过不写当前行
                        if record.split()[1] in line:
                            flag = 1
                            f.write( ' ' * 8 + record + '\n')
                            continue
                    # 对于不满足上述情况的行，全部覆盖写到配置文件中
                    f.write(line)
    # 如果flag仍为0，说明record中的IP不存在于backend现有的记录集中，调用add函数添加record
    if flag == 0:
        add(backend,record)
        print(ADD_RECORD_MSG)
    return True


def delete(backend,record):
    """
    用户输入4时调用，删除backend和记录
    :return: True 删除成功 False 要删除的内容不存在
    """
    # 调用backup函数得到配置文件的备份文件
    backup()
    # 调用check函数，如果backend已经存在于文件中，就将现有的backend记录返回
    serverList = check(backend)
    # 如果serverList为空，说明backend不存在，无法删除不存在的项，返回false
    if not serverList:
        return False
    # 如果record不存在于serverList中，无法删除不存在的项，返回false
    elif record not in serverList:
        return False
    # 否则要删的内容存在，开始删除
    else:
        with open(FILE_BAK, 'r', encoding='utf-8') as f_bak, open(FILE, 'w', encoding='utf-8') as f:
            # 如果serverList中元素不止1个，说明backend下面有多条记录，跳过要删除的record行即可
            if len(serverList) > 1:
                for line in f_bak:
                    if line.strip() != record:
                        f.write(line)
                    else:
                        continue
                return True
            # 否则，遇到record行或backend行就跳过，只将其余的行写入配置文件
            else:
                for line in f_bak:
                    if line.strip() == 'backend ' + backend:
                        continue
                    elif line.strip() == record:
                        continue
                    else:
                        f.write(line)
                return True


def backup():
    """
    用于备份，将haproxy.cfg备份到haproxy.cfg_bak
    :return: None
    """
    if not os.path.exists(FILE_BAK):
        open(FILE_BAK,'w',encoding='utf-8').close()
    with open(FILE_BAK,'w',encoding='utf-8') as f_bak,open(FILE,'r',encoding='utf-8') as f:
        for line in f:
            f_bak.write(line)


def main():
    """
    主函数
    :param option: 用户输入的选项
    :return: None
    """
    option = ''
    while option != 'q':
        # 打印规则信息
        print(RULE_MSG)
        # 提示用户输入选项
        option = input(OPTION_PROMPT)
        # 如果输入q就退出
        if option == 'q':
            exit()
        # 输入1 查看
        elif option == '1':
            backend = input(BACKEND_PROMPT.format(CHECK_MSG))
            result = check(backend)
            if result != []:
                # 打印提示信息，逐个打印获得的结果行
                print(RECORD_MSG.format(backend))
                for record in result:
                    print(record)
            else:
                print(NO_BACKEND_MSG)
            option = input(CONTINUE_PROMPT)
        # 输入2 添加
        elif option == '2':
            # 提示用户按指定格式输入要添加的内容
            print(CONTENT_MSG)
            content =input(RECORD_PROMPT.format(ADD_MSG))
            # 调用trans_content函数，如果输入合法，result = [backend,record],否则result = None
            result = trans_content(content)
            if not result:
                # 提示输入不合法
                print(INVALID_MSG)
                option = input(CONTINUE_PROMPT)
            else:
                backend = result[0]
                record = result[1]
                # 调用add函数将输入backend和record添加到配置文件
                flag = add(backend,record)
                if flag:
                    print(SUCCESS_MSG.format(ADD_MSG,backend,record))
                else:
                    print(DUPLICATE_CONTENT_MSG)
                option = input(CONTINUE_PROMPT)
        # 输入3 修改
        elif option == '3':
            print(CONTENT_MSG)
            content = input(RECORD_PROMPT.format(MODIFY_MSG))
            result = trans_content(content)
            if not result:
                # 提示输入不合法
                print(INVALID_MSG)
                option = input(CONTINUE_PROMPT)
            else:
                backend = result[0]
                record = result[1]
                # 调用backup函数，备份haproxy配置文件
                flag = modify(backend,record)
                if flag:
                    print(SUCCESS_MSG.format(MODIFY_MSG, backend, record))
                else:
                    print(DUPLICATE_CONTENT_MSG)
                option = input(CONTINUE_PROMPT)
        # 输入4 删除
        elif option == '4':
            # 提示用户按指定格式输入要添加的内容
            print(CONTENT_MSG)
            content = input(RECORD_PROMPT.format(DELETE_MSG))
            # 调用trans_content函数，如果输入合法，result = [backend,record],否则result = None
            result = trans_content(content)
            if not result:
                # 提示输入不合法
                print(INVALID_MSG)
                option = input(CONTINUE_PROMPT)
            else:
                backend = result[0]
                record = result[1]
                flag = delete(backend,record)
                if flag:
                    print(SUCCESS_MSG.format(DELETE_MSG, backend, record))
                else:
                    print(FAIL_DELETE_MSG)
                option = input(CONTINUE_PROMPT)
        # 输入4 备份
        elif option == '5':
            backup()
            print(BAK_MSG)
            option = input(CONTINUE_PROMPT)
        else:
            print(INVALID_MSG)


main()