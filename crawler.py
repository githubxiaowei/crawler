ng# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:21:06 2017

@author: Administrator
"""

import requests
from lxml import html
import re


#print(str(requests.get(url_root).content,'utf8'))

class crawler:
    def __init__(self, root, seed, re_list):
        self.url_root = root
        self.url_seed = seed
        self.to_visit = set(seed)
        self.visited = set()
        self.iter_times = -1
        self.stop_words = ['search','help','subtitle','comment','user','article']  
        self.re_list = re_list
        for idx in range(len(re_list)):
            with open('reg_'+str(idx),'w',encoding='utf8'):
                pass
        
    def gen_next(self):
        while(True):
            if(self.iter_times==0 or len(self.to_visit) == 0):
                print('end')
                yield ''       
            else:  
                self.iter_times -= 1
                print('times to iterate:',self.iter_times)
                yield self.to_visit.pop()
    
    def drop(self,url):
        if(url in self.visited):
            return True
        if(self.url_root not in url):
            return True
        for word in self.stop_words:
            if(word in url):
                return True
        return False
    
    def parse(self, url):
        print('visiting',url)
        self.visited.add(url)   
        response = requests.get(url)
        selector = html.fromstring(response.content)
        self.re_findall(response.text)
        hrefs = selector.xpath('//a/@href')   
        if(hrefs):
            for h in hrefs:
                if(h[0] == '/'):
                    href = self.url_root + h
                if(not self.drop(href)):        
                    self.to_visit.add(href)              
    
    def re_findall(self,content):
        for i,r in enumerate(self.re_list):
            self.re_log(i,r.findall(content))
    
    def run(self):
        for url in self.gen_next():
            if(url==''):
                break
            self.parse(url)
    
    def re_log(self,idx,find_list): 
        if(find_list):
            with open('reg_'+str(idx),'a',encoding='utf8') as f:
                for i in find_list:
                    f.write(i+'\n')
    
 
if __name__ == '__main__':
    reg = re.compile(r'rss/feed/[\d]+')
    root = 'http://www.zimuzu.tv'  
    seed = 'http://www.zimuzu.tv/'             
    crawler(root,seed,re_list=[reg]).run()
     


