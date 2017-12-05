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
    def __init__(self,fpath=''):
        self.fpath = fpath #该参数为搜索文本保存路径
        self.reList = [] #正则模板集合
        self.matchList = [] #匹配结果集合
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }
        self.stopwords = ['是','什么','谁','在','哪里','哪','一个']
        self.rules = { #替换规则
            '什么':['[一-龥]+'],
            '谁':['[一-龥]+'],
            '在 哪里':['在 [一-龥]+','位于 [一-龥]+'],
            '谁 是':['[一-龥]+ 担任','[一-龥]+ 获得]'],
            '哪 一个':['[一-龥]+']
        }
        if(fpath):
            with open(self.fpath,'w'):
                pass
        
    def search(self,query): #在百度中搜索,进一步访问前十个结果
        self.reList = self.gen_pattern(query)
        query = self.clean(query)
        url = 'http://www.baidu.com/s?ie=utf-8&wd='+query
        resp = requests.get(url,headers=self.headers)
        #print(str(resp.content,'utf8'))
        resultList = self.parse(resp)
        for url in resultList:
            self.extractText(url)
            
        return self.matchList
    
    def search_baike(self,query): #在百科中搜索
        self.reList = self.gen_pattern(query)
        for word in jieba.cut(self.clean(query)):
            url = 'https://baike.baidu.com/item/'+word
            self.extractText(url)        
        return self.matchList
        
        
    def parse(self,resp): #返回百度结果中前十的网页
        selector = html.fromstring(resp.content)
        return selector.xpath('//h3/a/@href')
    
    def extractText(self,url): #从网页文本中匹配
        try:
            print('访问: ',url)
            resp = requests.get(url,headers=self.headers)
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
            
    def gen_pattern(self, str): #构造匹配模板
        str = ' '.join(jieba.cut(str))
        print('分词: ',str)
        patternList = []
        for k in self.rules:
            if(k in str):
                for v in self.rules[k]:
                    patternList.append(re.compile(str.replace(k,v)))
        print('正则表达式: ',patternList)
        return patternList
    
    def clean(self, query): #除去停用词
        for word in self.stopwords:
            query = query.replace(word,'')
        print('查询请求: ',query)
        return query


if(__name__=='__main__'):
    begin = time.time()
    print(BaiduCrawler().search('伟大领袖是谁'))
    #print(BaiduCrawler().search_baike('伟大领袖是谁'))
    print('-'*20)
    print('用时 {} s'.format(time.time()-begin))
   
'''
分词:  伟大领袖 是 谁
正则表达式:  [re.compile('伟大领袖 是 [一-龥]+')]
查询请求:  伟大领袖
访问:  http://www.baidu.com/link?url=5U9h_kIHaRd2e2ilLA46-eXf6Uq29ELFbW7BnK-NI3JpUl4InvKoFGqILoovuAw0L4kogO3pbxLV2IA_YvO6Y_
访问:  http://www.baidu.com/link?url=fIINkV_V1z1r0EhNwTS5FVqgVVujGoX07Zy2nHc4G7V8BwSlEELmPCYkiBrWQCOHPITQJInJ2lwZ4YG-Ed6Ly2o6Iov7mMIGWti0xFyC01bxOZS7XXR5N8BlrwGnKw7wfpV8LfZxc6HnxKsR2Dq_0_
访问:  http://www.baidu.com/link?url=WVduMuzBF8EuhbKC36rozLwd_SGDBtOFwtwkytDfPa0zQ_TAgoA3st3accUVm8KLr57CPxZt_gMTkccUUvOe4a
访问:  http://www.baidu.com/link?url=9c3Ea1MPFq4_KG_qcTFYpl9XccTaYQmGFlQ8YQtcCB88eg9nh5asU2YYkvp0rQByGEPRRWQCBnf1iD3VT5cF3a
访问:  http://www.baidu.com/link?url=GzImZjGyg5DuuepvP7JylZbRxn-H7A1Xrc80-63Ol1hzkzHHrdyh2ImDKaxofO0gGbxcJxfaCTA0yLJDev_IBXoNL60K0otdCCSo02iooAXN7vOm9OJJbfeZY-PPH6miyFlqpQKBKIZ9LSExBDxFFp3pHMUhluQDo5LQtGkoWQu8NSWhzsvmyLxYnyaXBPrxm6P1adTJvbNuLcROIi2V2a
访问:  http://www.baidu.com/link?url=TrUXeql6CWJXujPCM6gSl2WG-wG1DExo5WVWZFopj9_O4xGoUqJcXSbdf4IXcz9kzbaIKlqdsATKgqvSNEmSJK
访问:  http://www.baidu.com/link?url=cW_qn3saKzug5Nog1SCo1kC0kwriieXPnUV2CCe4TNbESEqkLREIhEoMuWbprxwfm8Pc6JHFJOodbZPcl2RCqII4-5byV0V3G-x9rf_gBzG
访问:  http://www.baidu.com/link?url=NOuKilTAaUBf1IO_rAhBFSeLj5jaq7Nd3RXPWsl66LEikixT3LSKREngqW8oXwvaCwlOjy5VvvnNxTejQqjsFjIoNzGvIWOVdiqXcwYLKS7
访问:  http://www.baidu.com/link?url=FvKnM3I3vvuuYwEii5xuCxTaRsIAmtXQuNrk1FhdR5qwM0DXho2TiuMfR2BTBmcPp1K8pnuyw9A-IxSuuYCTl_
访问:  http://www.baidu.com/link?url=Qco8eJjwdiRhrSrh7eyAArDTcRvsy5T_cUl3Sj__kb7iF6P_DDvSrjgsW1zvKufI-ii2xbPKtmNKt-JZe8l16AZqDEcoR9K3pD-JWUHfJuG
['伟大领袖 是 恶魔', '伟大领袖 是 谁']
--------------------
用时 7.90255069732666 s
'''