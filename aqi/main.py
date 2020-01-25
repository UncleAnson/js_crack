#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/25 5:50 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import execjs
import requests

node = execjs.get()

# Params
method = 'GETCITYWEATHER'
city = '北京'
type = 'HOUR'
start_time = '2018-01-25 00:00:00'
end_time = '2018-01-25 23:00:00'

# Compile javascript
file = 'jsCode.js'
ctx = node.compile(open(file).read())
#
# # Get params
# js = 'getPostParamCode("{0}", "{1}", "{2}", "{3}", "{4}")'.format(method, city, type, start_time, end_time)
# params = ctx.eval(js)
#
# print(params)


with open('./jsCode.js', 'r', encoding='utf-8') as f:
    node = execjs.compile(f.read())
params = node.call("getPostParamCode", method, city, type, start_time, end_time)
print(params)
print('-' * 20)
# 发起post请求
url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
response_text = requests.post(url, data={'d': params}).text
print(response_text)
print('-' * 20)
# 对加密的响应数据进行解密
# js = 'decodeData("{0}")'.format(response_text)
# decrypted_data = ctx.eval(js)
decrypted_data = node.call("decodeData", response_text)
print(decrypted_data)
