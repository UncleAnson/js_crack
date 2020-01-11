#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 4:36 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


import requests

url = "https://passport.migu.cn/password/publickey"

raw_headers = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 0
Cookie: mgnd_session_id=ADARVEAXK2-GI7CVI911XF3VBSL4UFH2-MDJ8L35K-0; mgnd_session_create=1578384262426; mgpt_session_id=ADARIW9YK2-GI7CMYY11KFNNBBG06873-6HJ8L35K-0; mgpt_session_create=1578384262554; mgpt_session_last_access=1578385347395; LTToken=TGnid0000001578385379409Q0pIYffbwc2Y6FI24Jej4xBoQleyZGNO; USessionID=UDnid0000011578385379404KV4E63vrr20Pw5I2ltSqdnRjQ2t3wUca; idmpauth=true@passport.migu.cn; mgnd_session_last_access=1578385429899
Host: passport.migu.cn
Origin: https://passport.migu.cn
Pragma: no-cache
Referer: https://passport.migu.cn/login?sourceid=203021&apptype=2&forceAuthn=true&isPassive=false&authType=&display=&nodeId=70027513&relayState=login&weibo=1&callbackURL=http%3A%2F%2Fwww.miguvideo.com%2Fmgs%2Fwebsite%2Fprd%2Findex.html%3FisIframe%3Dweb
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
X-Requested-With: XMLHttpRequest'''
headers = dict([line.split(": ", 1) for line in raw_headers.split("\n")])

r = requests.post(url, headers=headers)
print(r.text)  # 获取生成publickey相关参数
