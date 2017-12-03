# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 23:00:11 2017

@author: Administrator
"""

import requests
import re
from crawler import crawler
'''
resources = []
reg = re.compile(r'/resource/[\d]+')
for i in range(1,614):
    print(i)
    url = 'http://www.zimuzu.tv/resourcelist/?page='+str(i)+'&channel=&area=&category=&year=&tvstation=&sort='
    text = requests.get(url).text
    resources.extend(reg.findall(text))
resources = set(resources)
with open('resourcelist','w',encoding='utf8') as f:
    for i in resources:
        f.write('http://www.zimuzu.tv'+i+'\n')
'''
class RssCrawler(crawler):
    def parse(self,url):
        print('visiting',url)
        self.visited.add(url)   
        response = requests.get(url)
        self.re_findall(response.text)
        
reg = re.compile(r'rss/feed/[\d]+')
root = ''  
seed = []             
with open('resourcelist',encoding='utf8') as f:
    for line in f.readlines():
        seed.append(line.strip('\n'))
        
RssCrawler(root,seed,re_list=[reg]).run()
    