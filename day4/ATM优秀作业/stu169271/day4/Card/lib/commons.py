#!/usr/bin/env python
# encoding: utf-8



import hashlib


def md5(arg):
    """
    md5加密
    :param arg: 要进行加密的字符串
    :return: 加密完成的字符串
    """
    obj = hashlib.md5()
    obj.update(bytes(arg, encoding='utf-8'))
    return obj.hexdigest()
