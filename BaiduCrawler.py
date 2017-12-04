# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 17:00:34 2017

@author: https://github.com/githubxiaowei

"""
#from crawllib import save_text
import requests
from lxml import html
import re
import jieba
import time

class BaiduCrawler:
    def __init__(self,fpath='result.txt'):
        self.root = 'http://www.baidu.com'
        self.fpath = fpath
        self.reList = []
        self.matchList = []
        self.stopwords = ['是','什么','谁','在','哪里']
        if(fpath):
            with open(self.fpath,'w'):
                pass
        
    def search(self,query):
        self.reList = self.gen_pattern(query)
        query = self.clean(query)
        url = self.root+'/s?ie=utf-8&wd='+query
        resp = requests.get(url)
        #save_text(resp,'result')
        #print(str(resp.content,'utf8'))
        resultList = self.parse(resp)
        for url in resultList:
            #print(url)
            self.extractText(url)
            
        return self.matchList
        
        
    def parse(self,resp):
        selector = html.fromstring(resp.content)
        return selector.xpath('//h3/a/@href')
    
    def extractText(self,url):
        try:
            
            with requests.Session() as s:
                s.max_redirects = 3
                resp = s.get(url)
            selector = html.fromstring(resp.content)
            result = re.sub('\s','',
                    ''.join(selector.xpath('//body//*[name(.)!="script" and name(.)!="style"]/text()')))+'\n'
            for pattern in self.reList:
                self.matchList.extend(pattern.findall(' '.join(jieba.cut(result))))

            if(self.fpath):
                with open(self.fpath,'a',encoding='utf8') as f:
                    f.write(result)
                
        except Exception as e:
            print(e)
            
    def gen_pattern(self, str):
        str = ' '.join(jieba.cut(str))
        patternList = []
        rules = {
                '什么':['[一-龥]+'],
                '谁':['[一-龥]+'],
                '哪里':['[一-龥]+'],
                '谁 是':['[一-龥]+ 担任','[一-龥]+ 获得']
                }
        for k in rules:
            if(k in str):
                for v in rules[k]:
                    patternList.append(re.compile(str.replace(k,v)))
        print('正则表达式: ',patternList)
        return patternList
    
    def clean(self, query):
        for word in self.stopwords:
            query = query.replace(word,'')
        print('查询请求: ',query)
        return query


if(__name__=='__main__'):
    begin = time.time()
    print(BaiduCrawler().search('东方之珠是哪里'))
    print('-'*20)
    print('用时 {} s'.format(time.time()-begin))
   
