# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:05:33 2017

@author: https://github.com/githubxiaowei
"""

import requests
from lxml import html


def today_list():
    url = 'http://www.zimuzu.tv/'
    response = requests.get(url)
    selector = html.fromstring(response.content)
    td_list = []
    for a in selector.xpath("//div[@class='fr today-play']//div[@class='box list']//a[@title]"):
        td_list.append(a.xpath('strong/text()')[0]+a.xpath('text()')[0])
    
    return td_list

rss_list = []
with open('reg_0',encoding='utf8')as f:
    for line in f.readlines():
        rss_list.append(int(line.split('/')[-1]))

with open('resources.csv','w',encoding='utf8') as f:
    f.write('description,filename,ed2k,magnet,pan,\n')

for p in rss_list:
    url = 'http://diaodiaode.me/rss/feed/' + str(p)
    print(url)
    response = requests.get(url,)
    selector = html.fromstring(response.content)
    
    resources = []
    for item in selector.xpath('//item'):
        info = {}
        #info['url'] = url
        #info['description'] = item.xpath('description/text()')
        info['filename'] = ' '.join(item.xpath('title/text()'))
        info['ed2k'] = ' '.join(item.xpath('ed2k/text()'))
        info['magnet'] = ' '.join(item.xpath('magnet/text()'))
        info['pan'] = ' '.join(item.xpath('pan/text()'))
        resources.append(info)

    with open('resources.csv','a',encoding='utf8') as f:
        for item in resources:
            line = ''
            for k in item:
                line += str(item[k])+','
            f.write(line+'\n')
    #csv should be resaved as UTF8 with BOM before load by EXCEL
    




