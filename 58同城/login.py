#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 10:00 上午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import requests

# 获得token
url = "https://passport.58.com/58/login/init?source=58-default-pc&path=http%253A%252F%252Fmy.58.com%252F%253Fpts%253D1578448732418&psdk-d=jsdk&psdk-v=1.0.2&callback=JsonpCallBack1578448679312604"
r = requests.get(url)
print(r.text)

# 获得rsa
url = "https://passport.58.com/58/rsa?source=58-default-pc&psdk-d=jsdk&psdk-v=1.0.2&callback=JsonpCallBack1578450734460476"
r = requests.get(url)
print(r.text)

# 获得fingerprint
url = "https://cdata.58.com/btData"
r = requests.get(url)
print(r.cookies)