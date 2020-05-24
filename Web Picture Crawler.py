# -*- coding: utf-8 -*-
"""
Created on Sun May 24 09:21:10 2020

@author: CILENCE_AIR
"""

import requests
import re
import time
import os

dir_name = 'E:/Desktop/python web/download/'

headers1={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
m=0
max_index=0

#定义连续下载的写真集数目
iteratormax=10


start_index = 17375 #设置起始页面ID
#循环iterator个页面
for i in range(iteratormax):
    
    response = requests.get('https://www.meitulu.com/item/'+str(start_index)+'.html',headers=headers1)
    html=(response.text)
    urlnew=re.findall('.html".[0-9]*<',html)
    max_index=re.sub("\D","",urlnew[-1])
#    print(max_index)
    for k in range(int(max_index)):
        if k==0:
            response1 = requests.get('https://www.meitulu.com/item/'+str(start_index)+'.html',headers=headers1)
        else:
            response1 = requests.get('https://www.meitulu.com/item/'+str(start_index)+'_'+str(k+1)+'.html',headers=headers1)

        
        
        html1 = response1.text
        urls=re.findall('https://img.*?.jpg',html1)
        urlscopy=list(urls)
        #去除链接小图杂图
        for j in urlscopy:
            if not str(start_index) in j:
                urls.remove(j)
#                print("删除杂图链接"+j) #debug
        
        
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        
        for url in urls:
            time.sleep(0.1)
            m=m+1
            file_name = url.split('.')[-1]#提取照片格式
            responsegraph =  requests.get(url,headers=headers1)
            with open(dir_name+'/'+'第'+str(m)+'张照片.'+file_name,'wb') as f:
                f.write(responsegraph.content)
                f.close()
                print('第'+str(m)+'张图片已下载')
           
    start_index =start_index+1
print('已下载'+str(m)+'张')











    
    


    