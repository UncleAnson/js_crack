#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 5:31 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

gov_depts = ["卫生健康委网站"]


def return_tag(title, tag, source):
    if "组织会" in title or "小组会" in title:
        return "国务院-会议-组织会议"
    elif "常务会" in title:
        return "国务院-会议-常务会议"
    elif "会议" in title:
        return "国务院-会议-会议"
    elif "通知" in title:
        return "国务院-政策文件-通知"
    elif "解读" in title and "《" in title:
        return "国务院-政策文件-解读"
    elif "公告" in title:
        return "国务院-政策文件-公告"
    elif source in gov_depts or "《" in title:
        return "国务院-政策文件-其他"
    else:
        return tag


def get_cookie(url):
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    cookies = driver.get_cookies()
    driver.quit()
    items = []
    dict_ = {}
    for i in range(len(cookies)):
        cookie_value = cookies[i]
        item = cookie_value['name'] + '=' + cookie_value['value']
        items.append(item)
        dict_[cookie_value['name']] = cookie_value['value']
    cookiestr = '; '.join(a for a in items)
    print(cookiestr)
    # return cookiestr
    return dict_


if __name__ == '__main__':
    pass
