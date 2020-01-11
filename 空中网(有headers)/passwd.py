#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 3:53 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import requests
raw_headers = '''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: SESSION_COOKIE=105; trackingId=46d20de4-212d-4224-8bf2-3ee526cbf921; kzu-er=13143410819; SSO-KGZQRT=69C2421AE1EEFC9DEAE50870326A23F6; Hm_lvt_1287c2225a527abe3386233dd9316f99=1578381105; Hm_lpvt_1287c2225a527abe3386233dd9316f99=1578381580; SSO-KGZLT=03836a75-004e-4769-b347-d94c8c126a9a; SSO-KGZIT=6f6c4f35-d376-4d21-ac3e-e148818036b7
Host: sso.kongzhong.com
Pragma: no-cache
Referer: https://passport.kongzhong.com/login
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'''
headers = dict([line.split(": ",1) for line in raw_headers.split("\n")])

url = "https://sso.kongzhong.com/ajaxLogin?j=j&&type=1&service=https://passport.kongzhong.com/&username=13143410819&password=31e40d24b97ea5c4028e874e&vcode=q5er&toSave=0&_=1578383251286"
r = requests.get(url, headers=headers)
print(r.text)