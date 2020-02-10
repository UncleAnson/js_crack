#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/8 10:33 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :
'''


selenium获取cookie，防识别检测

'''
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# browser = webdriver.Chrome(options=option)
# browser.get("http://www.nhc.gov.cn/xcs/kpzs/list_gzbd_5.shtml")
# print(browser.get_cookies())
import re


def get_cookie(url):
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    cookies = driver.get_cookies()
    # driver.quit()
    items = []
    for i in range(len(cookies)):
        cookie_value = cookies[i]
        item = cookie_value['name'] + '=' + cookie_value['value']
        items.append(item)
    cookiestr = '; '.join(a for a in items)
    return cookiestr


c = get_cookie("http://www.nhc.gov.cn/xcs/kpzs/list_gzbd_5.shtml")
print(c)

import requests

quanguo_headers = {
    'Cookie': 'yfx_f_l_v_t_10006654=f_t_1581181186938__r_t_1581181186938__v_t_1581181186938__r_c_0; yfx_c_g_u_id_10006654=_ck20020900594619416910081107112; security_session_verify=4c66fd3ffead9a6e85ff20b0be9c31ef; insert_cookie=98184645; oHAcoULcWCQb80T=4LnglMLKzi1enVBmbx08UT6MGBaVFMl6TkvoknHXwMib9gRfT8OTIM9LVYiu.MpvSPABi2XJLTIPrSVOsgBlqeaQXdsgvBB1LROnT5dTgZYWfUe8j9raGUoVFkOr.wNWtfuP7Jw2uqw0K3j5M1ZJRnZQWbuzYGMvp_chY7y_TsPYlLvYpFAFpHROnclJbr.xziQVl2k6VNuzfCRoLh.iiGxquNHRRDCEcC7Fk2hyY3C3XsVXCOB5PQB1vX9B2RUS3gGca9YAgwFv6WDCtiDnYSZYSKD4VD_jUQIr8ZBsUkD7GyJ3bfrKoabxYzr_qhDQWpwQ; oHAcoULcWCQb80S=4ECtQi5PVqfPliMVkjdYEOnMIKN7Dull82YarWq756DQk3K74ShdvuNh4XvPLZVq'}
quanguo_headers['Cookie'] = c
r = requests.get("http://www.nhc.gov.cn/xcs/kpzs/list_gzbd_5.shtml", headers=quanguo_headers)
print(r.status_code)

print(re.findall(r"'page_div',(\d+), (\d+),'", r.text))
