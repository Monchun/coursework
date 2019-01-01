import requests
import json
import time
import datetime
import sys
import random
reload(sys)
sys.setdefaultencoding('utf8')
class maoyan():
    def __init__(self,movieid=None,endPoint='2018-07-23 00:00:00'):
        self.movieid=movieid
        self.offset=0
        self.limit=15
        self.userid=-1
        self.ts=1545197450772
        self.now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.endPoint=endPoint
        self.headers=[a.strip() for a in open('/home/monchu/Data/assignments/user-agent','r').readlines()]
        self.url='http://m.maoyan.com/mmdb/comments/movie/249342.json'
        self.param={
            'offset':self.offset,
            '_v_':'yes',
            'startTime':self.now,
        }
        self.hasMore=True
        self.link=None
    def retrieveData(self):
        try:
            content=requests.get(self.url,headers={'User-Agent':random.choice(self.headers)},params=self.param)
            time.sleep(random.randint(0,1))
            print content.url
            if content.status_code==200:
                return content.content
        except Exception:
            time.sleep(random.randint(0,2))
            content=requests.get(self.url,headers={'User-Agent':random.choice(self.headers)},params=self.param)
            if content.status_code==200:
                return content.content
        else:
            print 'fail'
    def dataParser(self,content):
        if content!=None:
            print 'content retrieved'
            try:
                json_data=json.loads(content,encoding='utf-8')
            except ValueError as e:
                time.sleep(60)
                return e
            #self.param['ts']=json_data['ts']
            #if json_data['paging']['hasMore']=='true':
            #    self.hasMore=True
            #else:self.hasMore=False
            comments=[]
            try:
                for d in json_data['cmts']:
                    comment={
                        'nickName':d['nickName'] if 'nickName' in d else '',
                        'cityName':d['cityName'] if 'cityName' in d else '',
                        'content':d['content'].strip().replace('\n',''),
                        'score':d['score'],
                        'startTime':d['startTime'],
                        'filmView':str(d['filmView']) if 'fil,View' in d else '',
                        'gender':str(d['gender']) if 'gender' in d else '',
                    }
                    comments.append(comment)
                #print comments
                return comments
            except Exception as e:
                return e
            finally:
                pass            
        else:
            print None
            return None
    def worker(self):
        while self.param['startTime']>self.endPoint:
            print 'crawling 15 data before {}'.format(self.param['startTime'])
            content=self.retrieveData()
            comments=self.dataParser(content)
            if comments in ['nickName','cityName','content','score','startTime','filmView','gender'] or comments==ValueError:
                timestamp=time.mktime(time.strptime(self.param['startTime'],'%Y-%m-%d %H:%M:%S'))
                self.param['startTime']=datetime.datetime.fromtimestamp(timestamp)+datetime.timedelta(minutes=-2)
                continue
            elif comments!=None:   
                self.param['startTime']=comments[-1]['startTime']
                for item in comments:
                        #print item
                        with open('/home/monchu/Data/assignments/aquamanComments.txt','a') as f:
                            f.write(item['nickName']+'\t'+item['cityName']+'\t'+item['content']+
                            '\t'+str(item['score'])+'\t'+item['startTime']+'\t'+str(item['filmView'])+'\t'+item['gender']+'\n')
            else:print None
    def run(self):
        self.worker()
scarper=maoyan(movieid='249342')
scarper.run()
