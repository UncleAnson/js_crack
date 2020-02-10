#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/10 12:06 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :

import pandas as pd
import pymysql

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'godb'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'linyuepeng'
MYSQL_PORT = 3306

con = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                      user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                      db=MYSQL_DATABASE)
cur = con.cursor()

sql = 'SELECT * FROM godb.article_yiqing where tag like "%疫情通报%" order by pub_time desc;'
cur.execute(sql)

data_dict = []
for field in cur.description:
    data_dict.append(field[0])

data = pd.DataFrame(list(cur.fetchall()), columns=data_dict)
# print(data[['pub_time','content']])

import re


def extract(text=None):
    if text is None:
        text = text1
    # text = text.split()[0]
    print(text)
    subtext = re.search(r'(新增)?\w{0,}确诊病例(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("新增确诊：", subtext)

    subtext = re.search(r'新增治愈出院(病例)?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("新增治愈：", subtext)

    subtext = re.search(r'新增重症病例(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(1, 3)
    else:
        subtext = None
        # if "重症" in text:
        #     raise
    print("新增重症：", subtext)

    subtext = re.search(r'新增死亡(病例|患者)?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("新增死亡：", subtext)

    subtext = re.search(r'新增疑似病例(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(1, 3)
    print("新增疑似：", subtext)

    subtext = re.search(r'截至.*?累计\w*?确诊(病例)?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("累计确诊：", subtext)
    subtext = re.search(r'截至.*?治愈出院\w*?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(1, 3)
    print("累计治愈：", subtext)
    subtext = re.search(r'截至.*?隔离治疗(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(1, 3)
    print("累计隔离治疗：", subtext)
    subtext = re.search(r'截至.*?重症(病例)?(\d+)例,(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("累计重症：", subtext)
    subtext = re.search(r'截至.*?死亡(病例)?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("累计死亡：", subtext)
    subtext = re.search(r'截至.*?疑似(病例)?(\d+)例(（[\w|、]{0,}湖北[省]?(\d+)例)?', text)
    if subtext:
        subtext = subtext.group(2, 4)
    print("累计疑似：", subtext)

    subtext = re.search(r'追踪\w*?(\d+)人', text).group(1)
    print("累计追踪：", subtext)

    subtext = re.search(r'解除医学观察\w*?(\d+)人', text).group(1)
    print("解除医学观察：", subtext)

    try:
        subtext = re.search(r'(\d+)\w*?(尚在|接受)医学观察', text).group(1)
    except:
        subtext = re.search(r'(尚在|接受)医学观察\w*?(\d+)人', text).group(2)
    print("尚在医学观察：", subtext)

    print('--------------')


if __name__ == '__main__':
    text1 = '''
    　　    　　2月8日0—24时，31个省（自治区、直辖市）和新疆生产建设兵团报告，新增确诊病例2656例（湖北2147例），新增重症病例87例（湖北52例），新增死亡病例89例（湖北81例，河南2例，河北、黑龙江、安徽、山东、湖南、广西各1例），新增疑似病例3916例（湖北2067例）。
　　当日新增治愈出院600例（湖北324例），解除医学观察的密切接触者31124人。
　　截至2月8日24时，据31个省（自治区、直辖市）和新疆生产建设兵团报告，现有确诊病例33738例（其中重症病例6188例），累计治愈出院病例2649例（黑龙江核减1例），累计死亡病例811例，累计报告确诊病例37198例（山西、黑龙江、河南、海南各核减1例），现有疑似病例28942例。累计追踪到密切接触者371905人，尚在医学观察的密切接触者188183人。
　　累计收到港澳台地区通报确诊病例53例：香港特别行政区26例（死亡1例），澳门特别行政区10例（治愈出院1例），台湾地区17例（治愈出院1例）。
  　　'''
    for i, (title, content) in enumerate(data[['title', 'content']].values.reshape(-1, 2)):
        if "武汉" in title or "湖北" in title:
            continue
        extract(content)
    # break
    # extract()
