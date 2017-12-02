# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from lxml import html

def save_html(url):
    response = requests.get(url)
    with open('download.html','w',encoding='utf8') as f:
        f.write(str(response.content,'utf8'))

def today_list():
    url = 'http://www.zimuzu.tv/'
    response = requests.get(url)
    selector = html.fromstring(response.content)
    td_list = []
    for a in selector.xpath("//div[@class='fr today-play']//div[@class='box list']//a[@title]"):
        td_list.append(a.xpath('strong/text()')[0]+a.xpath('text()')[0])
    
    return td_list



with open('resources.csv','w',encoding='utf8') as f:
    f.write('url,description,filename,ed2k,magnet,pan,\n')

for p in range(1):
    print(p)
    url = 'http://diaodiaode.me/rss/feed/' + str(p)
    response = requests.get(url)
    selector = html.fromstring(response.content)
    
    resources = []
    for item in selector.xpath('//item'):
        info = {}
        info['url'] = url
        info['description'] = item.xpath('description/text()')
        info['filename'] = item.xpath('title/text()')
        info['ed2k'] = item.xpath('ed2k/text()')
        info['magnet'] = item.xpath('magnet/text()')
        info['pan'] = item.xpath('pan/text()')
        resources.append(info)

    with open('resources.csv','a',encoding='utf8') as f:
        for item in resources:
            line = ''
            for k in item:
                line += str(item[k])+','
            f.write(line+'\n')
    #csv should be resaved as UTF8 with BOM before load by EXCEL
    




