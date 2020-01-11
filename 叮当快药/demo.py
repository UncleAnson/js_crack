#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 3:48 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


# commodity.html中脚本保存了分类的id，并构造了每次请求的的参数对象

import time
from hashlib import md5
def get_sign():
    timeStamp = time.time()
    localTime = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

    l = ["method", "orderTypeId", "orgcode", "pageNo", "pageSize", "plat", "platform", "shopId", "t", "v",
         "versionName"]
    t = {
        'method': 'ddsy.product.query.orgcode.product.list.b2c',
        'orderTypeId': '0',
        'orgcode': '010502,010503,010504,010505,010506,010507',
        'pageNo': '1',
        'pageSize': '100',
        'plat': 'H5',
        'platform': 'H5',
        'shopId': '-1',
        # 't': '2019-9-23 22:4:16',
        't': '{}'.format(strTime),
        'v': '1.0',
        'versionName': '3.2.0'
    }
    p = ''
    for i in range(0, 11):
        m = l[i]
        p += m + t.get(m)
    f = t['method'] + p + '6C57AB91A1308E26B797F4CD382AC79D'
    print(f)
    sign = md5value(f).upper()
    print(sign)
    return sign


def md5value(s):
    a = md5(s.encode()).hexdigest()
    return a

get_sign()