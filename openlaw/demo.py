#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/6 5:31 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


import execjs

user = "1047053860@qq.com"
password = "woainizhongguo135"

with open('./openlaw_login.js', 'r', encoding='utf-8') as f:
    login_js = execjs.compile(f.read())

keyEncrypt_password = login_js.call('keyEncrypt', password)

print(keyEncrypt_password)




