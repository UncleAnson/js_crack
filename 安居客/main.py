#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 5:45 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import requests
from lxml.html import etree
import re

headers = '''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
cookie: wmda_session_id_6289197098934=1578733054264-20942fbf-0292-ac92; wmda_uuid=5fbfe9ddacaa47cb6d29916d90594c51; wmda_visited_projects=%3B6289197098934; sessid=B4AE8632-5316-4A63-F311-CX0111170444; aQQ_ajkguid=B4AE8632-317B-D219-A19E-CX0111170444; lps=http%3A%2F%2Fuser.anjuke.com%2Fajax%2FcheckMenu%2F%3Ff%3Dlogin%26r%3D0.3907470493136358%26callback%3DloginObj.successCallBack%7Chttps%3A%2F%2Fwww.anjuke.com%2Fcaptcha-verify%2F%3Fcallback%3Dshield; ctid=13; twe=2; 58tj_uuid=2993bc65-83d1-4275-a366-d38d3b0397e6; init_refer=; new_uv=1; _ga=GA1.2.1847451842.1578733486; _gid=GA1.2.201576367.1578733486; als=0; new_session=0; __xsptplus8=8.1.1578733485.1578735699.5%234%7C%7C%7C%7C%7C%23%23P_ME2Ehn-xmnAV7vU17d9E730wYPo0d5%23; xzfzqtoken=r9cdWwj965JZzMO27yWONkMb3y7WKhT2CFhd76mJ%2FIsDeu2tTeAIez9tz%2FUYLHpkin35brBb%2F%2FeSODvMgkQULA%3D%3D
pragma: no-cache
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'''


def get_dict(_str):
    obj = dict([line.split(": ", 1) for line in _str.split("\n")])
    return obj


headers = get_dict(headers)

url = "https://www.anjuke.com/captcha-verify/?callback=shield"
resp = requests.get(url, headers=headers)
html = etree.HTML(resp.text)
session_id = html.xpath('//input[@name="sessionId"]/@value')[0]
print("session_id:", session_id)
import time

from PIL import Image
from io import BytesIO

url = "https://verifycode.58.com/captcha/getV3?callback=jQuery19103047525747165929_{time}&showType=embed&sessionId={session_id}&_={time}".format(
    time=int(time.time() * 1000), session_id=session_id)
resp = requests.get(url, headers=headers)  # get验证码
print(resp.text)
image_url = re.findall(r'"bgImgUrl":"(.*?)"', resp.text)[0]
print("image_url:", image_url)
responseId = re.findall(r'"responseId":"(.*?)"', resp.text)[0]
print("responseId", responseId)

url = "https://verifycode.58.com" + image_url
resp = requests.get(url, headers=headers)
# req.content是二进制的字符串 传化为file 的 io对象
f = BytesIO(resp.content)
image = Image.open(f)
with open('captcha.jpg', 'wb') as f:
    f.write(resp.content)

def get_position(image):
    image = image.resize((284, 160))
    image = image.convert('L')
    yuzhi = 150
    yuzhi2 = 40
    ll = 10
    for i in range(55, image.size[0] - 20):  # 260
        for j in range(0, image.size[1] - 20):  # 160
            flag = True
            for l in range(0, ll):
                pixel = image.getpixel((i, j)) - image.getpixel((i + 1, j + l))
                if pixel < yuzhi2: flag = False
                # pixel = image.getpixel((i - l, j))
                # if pixel<yuzhi:flag=False
            for l in range(0, ll):
                pixel = image.getpixel((i, j + l))
                if pixel < yuzhi: flag = False

            if flag:
                cropedimage = image.crop((i, j, i + 30, j + 30))
                return i - 7
print(get_position(image))

headers = '''accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
cookie: xxzl_deviceid=lz3rmv6MA5Clp0J1MG3UsNIKVtHNpA0%2FYc%2BsT8saTClIFqGu4MwLKfIkj6RKrXD6; id58=c5/nn14Zj600O+o18wnJAg==; xzuid=e1f9a679-a1e2-47ea-a1ac-c0cfed024f4f
pragma: no-cache
referer: https://www.anjuke.com/captcha-verify/?callback=shield
sec-fetch-mode: no-cors
sec-fetch-site: cross-site
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'''

headers = get_dict(headers)
url = "https://cdata.58.com/fpToken?callback=dpjsonp_05531484146186183"
resp = requests.get(url, headers=headers)
# print(resp.text)
token = re.findall(r'token":"(.*?)"', resp.text, re.S)[0]
print("token", token)
