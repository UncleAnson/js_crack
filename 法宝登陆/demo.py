#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 10:45 上午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :
'''

这不单单是份代码，也是份教程，做足了补充解释 by yp
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 提供判断的条件
from selenium.webdriver.common.by import By

proxies = {
    'https': 'http://127.0.0.1:1087',
    'http': 'http://127.0.0.1:1087'
}

chrome_options = Options()
# 去掉特征值
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--headless')
chrome_options.add_argument("–proxy-server=%s" % proxies)


class Crawler(object):
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def get(self, url):
        self.browser.get(url)
        # WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, "用户名称：")))

    def __del__(self):
        for fp in self.browser.window_handles:
            self.browser.switch_to_window(fp)
            self.browser.close()

    def execute(self, username, passwd, code):
        # 输入账号密码
        self.browser.find_element_by_id("password").send_keys(username)
        self.browser.find_element_by_id("username").send_keys(passwd)
        # 操作点击->登陆
        self.browser.find_element_by_name("Submit").click()
        # 等待页面空白跳转
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.presence_of_element_located((By.LINK_TEXT, '法律数据库')))
        '''
        验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw').
        一个只要一个符合条件的元素加载出来就通过；另一个必须所有符合条件的元素都加载出来才行.
        presence_of_element_located  
        presence_of_all_elements_located
        验证元素是否可见，前两个传入参数是元组类型的locator，第三个传入WebElement.第一个和第三个其实质是一样的  
        visibility_of_element_located  
        invisibility_of_element_located  
        visibility_of  
        '''
        # 通过文字去捕捉元素
        self.browser.find_element_by_link_text('法律数据库').click()
        # 通过xpath去捕捉元素
        self.browser.find_element_by_xpath('//a[@title="北大法宝"]').click()
        # 动态加载速度慢，等待ajax加载
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(./text(), "%s")]' % code)))
        self.browser.find_element_by_xpath('//a[contains(./text(), "%s")]' % code).click()
        # 新标签浏览，需要做句柄切换
        self.browser.switch_to_window(self.browser.window_handles[-1])
        # 等待跳转到官网
        WebDriverWait(self.browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "explain")))
        print(self.browser.title)
        print(self.browser.get_cookies())


if __name__ == '__main__':
    c = Crawler()
    c.get("http://www.key007.com/e/member/login/")
    c.execute("xx", "xx", "25833")
