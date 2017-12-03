# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:30:21 2017

@author: https://github.com/githubxiaowei
"""

import requests
from lxml import html
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import getpass

class DeanCrawler:
    def __init__(self):
        self.url_root = 'http://dean.pku.edu.cn/student/'
        self.phpsessid = ''
        self.sno = ''
        self.password = ''
        self.cookie = {}
        self.data = {'submit':'%B5%C7%C2%BC',}
        self.connected = False
        
    def setInfo(self,sno,password):
        self.data['sno'] = sno
        self.data['password'] = password
        return self
        
    def establish(self):
        resp = requests.get(self.url_root)
        selector = html.fromstring(resp.content)
        img_src = selector.xpath('//img[@id="img-captcha"]/@src')[0]
        resp = requests.get(self.url_root+img_src)
        PHPSESSID = resp.cookies['PHPSESSID']
        self.cookie['PHPSESSID'] = PHPSESSID
        img = Image.open(BytesIO(resp.content))
        plt.imshow(img)
        plt.show()
        num = input(u'验证码\n')
        self.data['captcha'] = num
        url = self.url_root+'authenticate.php'
        resp = requests.post(url,data=self.data,cookies=self.cookie)
        self.connected = bool(resp.status_code == 200)
    
    def visit(self,sub_url,encoding='utf8'):
        resp = requests.get(self.url_root+sub_url+'?PHPSESSID='+self.cookie['PHPSESSID'])
        print(str(resp.content,encoding))
        
if(__name__=='__main__'):   
    c = DeanCrawler()
    sno = input('student number: ')
    pwd = getpass.getpass('password: ')
    c.setInfo(sno,pwd).establish()
    if(c.connected):
        c.visit('menu.php')
        c.visit('new_grade.php')

    
    