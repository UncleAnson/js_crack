#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 10:00 上午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import requests

# 获得token
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "wmda_uuid=9d200b6825444624ebaf309c8361703c; wmda_new_uuid=1; wmda_session_id_10104579731767=1588732999760-d6f8faa8-615a-148e; wmda_visited_projects=%3B10104579731767; ppStore_fingerprint=6E6A9C3F1F563350E759A430BC33F41845D44C4506DB966A; finger_session=sStLWKDkEGZjxXx6nXAbgW9OmUQZ6V46",
    "Host": "passport.58.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://passport.58.com/login",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
}
url = "http://passport.58.com/58/login/init?source=58-default-pc&path=http%253A%252F%252Fmy.58.com%252F%253Fpts%253D1588734593493&psdk-d=jsdk&psdk-v=1.0.3&callback=JsonpCallBack1588734560195501"
# r = requests.get(url,headers=headers)
# print(r.text)

# 获得rsa（rsaModulus、rsaExponent）
url = "https://passport.58.com/58/rsa?source=58-default-pc&psdk-d=jsdk&psdk-v=1.0.2&callback=JsonpCallBack1578450734460476"
r = requests.get(url)
print(r.text)
#
# 获得fingerprint
# 下面是直接复制上面的headers，只是cookie去掉了后面两个，如果存在，则不会新写入cookies
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "wmda_uuid=9d200b6825444624ebaf309c8361703c; wmda_new_uuid=1; wmda_session_id_10104579731767=1588732999760-d6f8faa8-615a-148e; wmda_visited_projects=%3B10104579731767",
    "Host": "passport.58.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://passport.58.com/login",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
}
url = "http://passport.58.com/sec/58/fingerprint?source=58-default-pc&finger2=zh-CN%7C24%7C2%7C4%7C1440_900%7C1440_900%7C-480%7C1%7C1%7C1%7Cundefined%7C1%7Cunknown%7CMacIntel%7Cunknown%7C3%7Cfalse%7Cfalse%7Cfalse%7Cfalse%7Cfalse%7C0_false_false%7Cd41d8cd98f00b204e9800998ecf8427e%7C21d802723147cc29b8be7114f5451e7a&psdk-d=jsdk&psdk-v=1.0.3&callback=JsonpCallBack1588735769007668"
r = requests.get(url, headers=headers)
print(r.cookies)
'''
<RequestsCookieJar[<Cookie finger_session=C91n35YZbnNw4NuJ0h6sBhgogOaUqsNn for .passport.58.com/>, <Cookie ppStore_fingerprint=181B3117A7646492550B5DF897D403E4D4EA0CF9AB3A59AB for .passport.58.com/>]>
'''
