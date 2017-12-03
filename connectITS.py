# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 09:51:33 2017

@author: https://github.com/githubxiaowei
"""

from lxml import html
import requests
from getpass import getpass

sno = input('student number: ')
password = getpass('password: ')

d = {
	'username':sno,
	'password':password,
	'iprange':'yes'
	}

url = 'https://its.pku.edu.cn/cas/webLogin'

resp = requests.post(url,data=d)
selector = html.fromstring(resp.content)

try:
	name = selector.xpath('//li/text()')[0]
	print('登入成功, ',name)
except:
	print('连接失败')

