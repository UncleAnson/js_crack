#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/7 12:16 上午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "cds_session_id=9blcvu0fooe0p963soibrkd401; Hm_lvt_0cb325d7c4fd9303b6185c4f6cf36e36=1588779881; cds_asm_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDY2MzciLCJpYXQiOjE1ODg3ODA1MzQsImV4cCI6MTU5MTM3MjUzNH0.azA1866Y9-E8L9PgvtEO6eIb4C5l3RLcG37cdCt1618; Hm_lpvt_0cb325d7c4fd9303b6185c4f6cf36e36=1588825319",
    "Host": "www.chandashi.com",
    "Pragma": "no-cache",
    "Referer": "https://www.chandashi.com/apps/review/appId/1142110895/country/cn.html?referer=/apps/review/appId/1142110895/country/cn.html",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
import time
import execjs

with open("./test.js", "r") as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
t = int(time.time())
params = {
    "appId": "1142110895",
    "country": "cn",
    "startDay": "20200422",
    "endDay": "20200507",
    "type": "time",
    "page": "1",
    "clientId": "10005",
    "timestamp": "{}".format(t),
}
sign = ctx.call("signFuc", params)
print(sign, len(sign), True if len(sign) == 40 else False)
params["sign"] = sign
# 872055B7C8342125B6F7082308B78D704E7D7A
# 6D8FB189B7829A9BBA367E7A2C77A2ED37DB07B5
#
url = 'https://www.chandashi.com/Api/apps/reviewDatas'

resp = requests.get(url, headers=headers, params=params)
print(resp.json())
