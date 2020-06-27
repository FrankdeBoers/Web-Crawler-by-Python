# -*- coding: utf-8 -*-
"""
Created on Sun May 24 09:21:10 2020

@author: CILENCE_AIR
"""

import requests
import re
import time
import os
#from bs4 import BeautifulSoup

dir_name = 'E:/Desktop/python web/download/'

headers1={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
m=0
max_index=0

#定义连续下载的写真集数目
iteratormax=10
basehttp='https://ucp76.com'


response = requests.get('https://ucp76.com/index.html',headers=headers1)
response.encoding='gb2312'
html=response.text
find=re.findall('href=".*?套图\[\d*P\]',html)
pages=re.findall('href=.*?\.html',str(find))


for i in pages:
    a=re.findall(i+'.*?\[\d+P\]',str(find))#查找总图数量
    nums=int(re.sub('\D','',str(re.findall('\[\d+P\]',str(a)))))
    if nums%5!=0:
        pagenum=(nums-(nums%5))/int(5)+1
    else:
        pagenum=(nums-(nums%5))/int(5)
                  
    
    respnew=requests.get(basehttp+re.sub('href="','',str(i)),headers=headers1)
    respnew.encoding='gb2312'
    htmlnew=respnew.text
    figs=re.findall('<p><img src="http.*?-\d+\.jpg',str(htmlnew))
    
    for j in range(1,int(pagenum)):
        respnew1=requests.get(basehttp+re.sub('.html','',re.sub('href="','',str(i)))+'_'+str(j+1)+'.html',headers=headers1)
        respnew1.encoding='gb2312'
        htmlnew1=respnew1.text
        figsnew=re.findall('<p><img src="http.*?-\d+\.jpg',str(htmlnew1))
#        figs.append(figsnew)  append会把整体从尾部嵌入list中，展开嵌入需要使用extend（）
        figs.extend(figsnew)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    
    for url in figs:
        time.sleep(0.1)
        m=m+1
        try:#地址有误时抛出异常
            url=re.sub('<p><img src="','',url,)
        except Exception as err:
            print(url+'网址异常')
        
        file_name = url.split('.')[-1]#提取照片格式
        responsegraph =  requests.get(url,headers=headers1,timeout=600)
        responsegraph.raise_for_status()
        with open(dir_name+'/'+'第'+str(m)+'张照片.'+file_name,'wb') as f:
            f.write(responsegraph.content)
            f.close()
            print('第'+str(m)+'张图片已下载')

print('下载结束，总共下载'+str(m)+'张图片')











    
    


    
