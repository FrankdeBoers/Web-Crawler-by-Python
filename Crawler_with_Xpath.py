# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:26:40 2020

@author: CILENCE
"""


import requests
from lxml import etree
import re
import time
import os

dir_name = 'E:/Desktop/python web/download/XpathDown'
if __name__=="__main__":
    headers1={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple\
                WebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari\
                    /537.36'
                }
    response=requests.get('https://www.tupianzj.com/meinv/mm/siwayouhuo/',headers1)
    response.encoding='gbk'
    html=response.text
    tree=etree.HTML(html)
    pic_list=tree.xpath('//dl[@class="tbox"]/dd/ul/li')
    heji_list=[]
    for p in pic_list:
        href='https://www.tupianzj.com/'+p.xpath('./a/@href')[0]
        # print(href)
        if '.html' in href:
            heji_list.append(href)
            
    pic_list=[]
    for i in heji_list:
        response1=requests.get(i,headers1)
        response1.encoding='gbk'
        html1=response1.text
        treenew=etree.HTML(html1)
        pic=treenew.xpath('//div[@id="bigpic"]/a[2]/img/@src')
        pic_list.append(pic)
        pageslist=treenew.xpath('//div[@class="pages"]/ul/li[1]/a/text()')
        pages=int(re.sub('\D','',pageslist[0]))
        for m in range(pages-1):
            r=re.sub('.html','',i)
            response1=requests.get(r+'_'+str(m+2)+'.html',headers1)
            response1.encoding='gbk'
            html1=response1.text
            treenew=etree.HTML(html1)
            pic=treenew.xpath('//div[@id="bigpic"]/a[2]/img/@src')
            pic_list.append(pic)
            
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
   
    m=0
   for url in pic_list:
        time.sleep(0.1)#增加延迟
        m=m+1
        file_name = 'jpg'
        responsegraph =  requests.get(url[0],headers=headers1)
        with open(dir_name+'/'+'第'+str(m)+'张照片.'+file_name,'wb') as f:
            f.write(responsegraph.content)
            f.close()
            print('第'+str(m)+'张图片已下载')
   print('完成下载')
   
   
   
