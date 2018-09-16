import requests
from lxml import html
import re
import time
import random


class csdnCrawler:
    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            #'Connection': 'keep-alive',
            'Connection': 'close'
        }
        
    def click(self):
        url = 'https://blog.csdn.net/'+'你的csdn用户名'
        resp = requests.get(url,headers=self.headers)
        #print(str(resp.content,'utf8'))
        resultList = self.parse(resp)
        for url in resultList:
            self.visit(url)

    def parse(self,resp): #博客列表
        selector = html.fromstring(resp.content)
        return selector.xpath('//p[@class="content"]/a/@href')
    
    def visit(self,url):
        try:
            print('访问: ',url)
            resp = requests.get(url,headers=self.headers)
            selector = html.fromstring(resp.content)
                
        except Exception as e:
            print(e)
            


if(__name__=='__main__'):
    csdn = csdnCrawler()
    times = 0
    while(times < 1000):
        csdn.click()
        times = times+1
        print(times)
        time.sleep(60+random.random()*5)
