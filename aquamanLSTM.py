#/usr/bin/python
# -*- coding:utf-8 -*- 
import pandas as pd
import sys
import numpy as np 
import jieba
import re
reload(sys)
sys.setdefaultencoding('utf-8')
path='/home/monchu/Data/assignments/'
names=['id','city','comments','score','date','fileview','sex']
unique=pd.read_table(path+'/uniqueComments.csv',names=names,delimiter='\t')
new=pd.DataFrame()
for index,row in unique.iterrows():
    try:
        a=row['date'].split(' ')
        row['day']=a[0]
        row['hour']=a[-1].split(':')[0]
        new=new.append(row)
    except Exception:continue
new.to_csv('path'+'new.csv',index=False)