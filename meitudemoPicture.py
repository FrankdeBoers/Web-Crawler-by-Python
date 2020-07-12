# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 22:14:26 2020

@author: CILENCE
"""

import requests
from lxml import etree
import re
import time
import os
import threading

url='http://meitulu.92demo.com/t/wangyuchun/'
dir_name = 'E:/Desktop/python web/download/MeituDemo'
headers1={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; \
                Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom\
        e/83.0.4103.116 Safari/537.36'
            }


if not os.path.exists(dir_name):
     os.makedirs(dir_name)
     
     
def downloadPic(start,end,name_list,pic_list,dir_name):
    for x in range(start,end):
        try:
            time.sleep(0.2)
            responsegraph =  requests.get(pic_list[x],headers=headers1)
            with open(dir_name+'/'+name_list[x]+str(x+1)+'.jpg','wb') as f:#第0.jpg会报错
                f.write(responsegraph.content)
                f.close()
                print('第'+str(x)+'张图片已下载')
        except:
            print(pic_list[x]+'   下载有问题')
            continue

if __name__=='__main__':
    response=requests.get(url,headers1)
    response.encoding='utf-8'
    html=response.text
    tree1=etree.HTML(html)
    pic_list=tree1.xpath('//div[@class="boxs"]/ul/li')
    heji_list=[]
    
    for p in pic_list:
        href='http://meitulu.92demo.com'+p.xpath('./a/@href')[0]
        if '.html' in href:
            heji_list.append(href)
            
    
    pic_list=[]
    name_list=[]
    for i in heji_list:
        response1=requests.get(i,headers1)
        response1.encoding='utf-8'
        html1=response1.text
        treenew=etree.HTML(html1)
        pic=treenew.xpath('//div[@class="content"]/center/a/img/@src')[0]
        pic_list.append(pic)
        name=treenew.xpath('//div[@class="content"]/center/a/img/@alt')[0]
        name_list.append(name)
        pageslist=treenew.xpath('//div[@class="width"]/div/p[3]/text()')[0]
        pages=int(re.sub('\D','',pageslist))
        for m in range(pages-1):
            try:
                # r=re.sub('.html','',i)
                r=i.replace('.html','')
                response1=requests.get(r+'_'+str(m+2)+'.html',headers1)
                response1.encoding='utf-8'
                html1=response1.text
                treenew=etree.HTML(html1)
                pic=treenew.xpath('//div[@class="content"]/center/a/img/@src')[0]
                pic_list.append(pic)
                name=treenew.xpath('//div[@class="content"]/center/a/img/@alt')[0]
                name_list.append(name)
            except:
                print(r+'_'+str(m+2)+'.html'+'   有异常')
                continue
            
    
    threads=[]
    for a in range(0,len(pic_list),50):
        new=threading.Thread(target=downloadPic,args=(a,a+49,name_list,\
                                                      pic_list,dir_name))
        threads.append(new)
        new.start()
        
    for s in threads:
        s.join()
        
    print('完成！')
            
            
            
