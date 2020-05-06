#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 12:43 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import base64
import zlib
'''
原算法是使用zlib压缩后base64加密所有参数，生成_token
'''
import requests
import time

url = "https://i.waimai.meituan.com/openh5/homepage/poilist?_={TIME_NOW}&X-FOR-WITH={X_FOR_WITH}"

TIME_NOW = int(time.time())
X_FOR_WITH = ""

data = {
    "startIndex": "1",
    "sortId": "0",
    "multiFilterIds": "",
    "sliderSelectCode": "",
    "sliderSelectMin": "",
    "sliderSelectMax": "",
    "geoType": "2",
    "rankTraceId": "5E0375319143CA4F9A3FF0BB99825887",
    "uuid": "171e2dd39289-0504973b679969-38677b00-13c680-171e2dd3929c8",
    "platform": "3",
    "partner": "4",
    "originUrl": "https://h5.waimai.meituan.com/waimai/mindex/home",
    "riskLevel": "71",
    "optimusCode": "10",
    "wm_latitude": "22599344",
    "wm_longitude": "114115167",
    "wm_actual_latitude": "22599344",
    "wm_actual_longitude": "114115167",
    "openh5_uuid": "171e2dd39289-0504973b679969-38677b00-13c680-171e2dd3929c8",
    "_token": "eJxd0tmOokAYBeB34baJ1EIVlMlcaLeyuCC4M+kLRB1QcANEmMy7TxVmuns6IeHL4fxVpOC3dLO2UhsCqAEoS/fdTWpLsAVaVJKlPONPiK5TggDVAdZkKfzMMIAYYCRLm9viTWr/hKoKZB3Bd5F4PHgmDIB3+QuRyi/RsXhFivL8krUVJSKtMojTIG6luzgvglMrPKfKM1LS+LTdPZTonO74W0l8OJ2JYQ0TmTCk8lDD9IMq/GRTIIKkSWlDVVATpIgTI0FNUAWCuhhTmSATY0QspgONk4oxHYnd9CblW1AAoCAVRGIFXUecWOymM8ypkv/JYENRYEzlJE3K0DfihqJL0CfhJ8EHm/d9LvaVekPyjVpD+iQ/0KM4UH4PmoMV3wjJFu8gnckYIPnNWoha/q824r8Jf5zFv05cO7tK5qO8KA8dV+mGzv1irkOvNpNV2YG9yNKCEzj0Kt32/BfPIjM6Vlb9QXIdIJXdZm5d1FkdV04Ph6GVHe0izxLwiANrWUO739uUHXafZMyYhp3BAibe/LaI4ii9d2lgRu7Bi6fbwtDLiTEFQ+2S4cOyutNxwuxHhmd2Grvdwcitt6YK0SE5ji114s+S0rrWoyP1y3PfzhS7b8IH+QUup7vlDx3XNYO++9it48q7jhd0Cnt2lQ6qC0Pz/bKEvsXW2dm318P5duhcHc2IV+v9KqjMIL7Nc4/1R5dqq3arjLj+CBqFNVw6h1mi5ftq6FClY4xq8GoNZspr0Lv59WRzHXp7XKsbZ3NVqDmui5DWoTv0p4t5aS3zUCl2r5MxGbhp1DWME0k0qoVgqr50tnucwvKH9Ocvv/wCwg==",
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://h5.waimai.meituan.com",
    "Referer": "https://h5.waimai.meituan.com/waimai/mindex/home",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
}

r = requests.post(url, data=data, headers=headers).json()

shoplist = r["data"]["shopList"]
for s in shoplist:
    print(s["shopName"])

if __name__ == '__main__':
    pass
