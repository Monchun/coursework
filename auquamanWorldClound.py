#/usr/bin/python
# -*- coding:utf-8 -*- 
import pandas as pd 
import pyecharts
import re
import sys
import jieba
from string import punctuation
from collections import Counter
reload(sys)
sys.setdefaultencoding('utf-8')
add_punc='，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
all_punc=punctuation+add_punc
path='/home/monchu/Data/assignments/'
names=['id','city','comments','score','date','fileview','sex']
unique=pd.read_table(path+'uniqueComments.csv',names=names,delimiter='\t')
posteriorC=unique[unique['date']>'2018-12-07 00:00:00']['comments']
anteriorC=unique[unique['date']<'2018-12-07 00:00:00']['comments']
lp=len(posteriorC)
la=len(anteriorC)
stopWord=[a.strip() for a in open(path+'stopword/stopHEU.txt','r')]
posterior1=[re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),comment) for comment in posteriorC]
anterior1=[re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),comment) for comment in anteriorC]
posterior=[re.sub(r'\w+','',c) for c in posterior1]
anterior=[re.sub(r'\w+','',c) for c in anterior1]
jieba.enable_parallel(10)
pWordList=[word for word in jieba.cut(''.join(posterior),cut_all=False) if word not in stopWord and all_punc]
aWordList=[word for word in jieba.cut(''.join(anterior),cut_all=False) if word not in stopWord and all_punc]
jieba.disable_parallel()
pcounter=Counter()
acounter=Counter()
for w in pWordList:
    pcounter[w]+=1
for w in aWordList:acounter[w]+=1
pattr,pvalue=pyecharts.WordCloud.cast(dict(pcounter))
aattr,avalue=pyecharts.WordCloud.cast(dict(acounter))
wordCloud=pyecharts.WordCloud('WordCloud Generated with {} comments after 2018-12-07 00:00:00'.format(lp),width=1300,height=620)
wordCloud.add("",pattr,pvalue,word_size=[20,100],shaped='diamond')
wordCloud.render(path=path+'wordCloud.html')
wordCloud2=pyecharts.WordCloud('WordCloud Generated with {} comments before 2018-12-07 00:00:00'.format(la),width=1300,height=620)
wordCloud2.add("",aattr,avalue,word_size=[20,100],shape='diamond',)
wordCloud2.render(path=path+'wordCloud2.html')