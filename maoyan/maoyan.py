#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/22 2:00 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


import re
import requests
from lxml import etree
from fontTools.ttLib import TTFont
import numpy as np

# headers = {
#     "Host": "maoyan.com",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 "
#                   "Safari/537.36"
# }
# url = "https://maoyan.com/cinemas?movieId=42964"
# res = requests.get(url, headers=headers)
# woff_url = re.findall(r"vfile.*?woff", res.text)[0]
# font_name = 'online.woff'
# with open(font_name, 'wb') as f:
#     f.write(requests.get("http://" + woff_url).content)
#
# font1 = TTFont('base.woff')
# print(font1.keys())
# print(font1.getGlyphNames())
# print(font1.get("glyph00000"))

def dtw_distance(ts_a, ts_b, d=lambda x, y: abs(x - y), mww=10000):
    """Computes dtw distance between two time series

    Args:
        ts_a: time series a
        ts_b: time series b
        d: distance function
        mww: max warping window, int, optional (default = infinity)

    Returns:
        dtw distance
    """

    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i - 1, 0] + d(ts_a[i], ts_b[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j - 1] + d(ts_a[0], ts_b[j])

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - mww), min(N, i + mww)):
            choices = cost[i - 1, j - 1], cost[i, j - 1], cost[i - 1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

    # Return DTW distance given window
    return cost[-1, -1]

# 解析字体库
def parse_ttf(font_name):
    """
    :param font_name: 字体文件名
    :return: 字符-数字字典
    """
    base_nums = ['3', '0', '1', '6', '4', '2', '5', '8', '9', '7']
    base_fonts = ['uniF2DF', 'uniED0B', 'uniF17D', 'uniEA80', 'uniE504',
                  'uniF200', 'uniF1DE', 'uniE558', 'uniF343', 'uniF17B']
    font1 = TTFont('base.woff')  # 本地保存的字体文件
    font2 = TTFont(font_name)  # 网上下载的字体文件

    uni_list = font2.getGlyphNames()[1:-1]  # 去掉头尾的多余字符 "glyph00000" "x"
    print(uni_list)
    temp = {}

    # 解析字体库
    for i in range(10):
        uni2 = font2['glyf'][uni_list[i]]
        l2 = np.array(uni2.coordinates)[:,0].tolist()
        l = []
        for j in range(10):
            uni1 = font1['glyf'][base_fonts[j]]
            l1 = np.array(uni1.coordinates)[:, 0].tolist()
            l.append(dtw_distance(l2, l1))
        index = np.argmin(l)
        temp[uni_list[i]] = base_nums[index]
    return temp

if __name__ == '__main__':
    print(parse_ttf("online.woff"))