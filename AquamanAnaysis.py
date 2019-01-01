#/usr/bin/python
 # -*- coding:utf-8 -*- 
import pandas as pd 
from collections import Counter
import pyecharts
import re
import sys
import requests
import time
reload(sys)
sys.setdefaultencoding('utf-8')
def get_urt(addtress):
    queryStr = 'http://api.map.baidu.com/geocoder?'
    param={
        'key':'rNro0Ci5oU66GYxQhyb1sIN6P3iCr4NR',
        'output':'json',
        'address':addtress,
    } 
    r=requests.get(queryStr,params=param)
    return r
path='/home/monchu/Data/assignments/'
names=['id','city','comments','score','date','fileview','sex']
UniqueComments=pd.read_table('/home/monchu/Data/assignments/aquamanComments.txt','r',names=names,delimiter='\t')
cityCounter=Counter()
UniqueComments['city'].describe()
after=pd.DataFrame()
for index,row in UniqueComments.iterrows():
    if row['date']>'2018-12-07 00:00:00':
        try:
            city=unicode(row['city'],'utf-8')
            cityCounter[city]+=1
            #after=after.append(row)
        except:pass
#after.to_csv('/home/monchu/Data/assignments/Valuable.csv',sep='\t',index=False)
cityDict=dict(cityCounter)
attr,value=pyecharts.Geo.cast(cityDict)
geo= pyecharts.Geo("Distribution of Aquaman film commenters in China (Total comments:{})".format(sum(value)), "Data scraped from MaoYao.com; Before 2018-12-20 11:09:25", title_color="#fff", title_pos="center", width=1200, height=600,background_color='#404a59')
geo.add_coordinate_json('/home/monchu/Data/assignments/city2.json')
flag=True
i=0
geo.add_coordinate(u'伊犁',80.9,91.01)
geo.add_coordinate(u'杨凌',107.59,34.14)
geo.add_coordinate(u'海东',102.12,36.50)
geo.add_coordinate(u'海南州',99,36)
geo.add_coordinate(u'璧山',106.15,29.41)
geo.add_coordinate(u'锡林郭勒',116.23,43.23)
while flag:  
    try:
        geo.add("", attr, value,visual_range=[min(value),max(value)],is_piecewise=True,visual_text_color="#fff",symbol_size=6, is_visualmap=True,visual_split_numer=6)
        print "?"
        flag=False
    except Exception as e:
        toq=re.sub('(.*for )','',str(e))
        j=get_urt(toq).json()
        if len(j['result'])==0:
            print toq
            a=raw_input("经,纬").split(',')
            geo.add_coordinate(unicode(toq,'utf-8'),a[0],a[1])
            continue
        geo.add_coordinate(unicode(toq,'utf-8'),j['result']['location']['lng'],j['result']['location']['lat'])
        time.sleep(0.2)
        i+=1
        print i
    finally:pass
geo.render(path=path+'heatmap of filmviewer.html')
