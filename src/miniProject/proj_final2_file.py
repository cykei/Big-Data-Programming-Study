#encoding:utf-8
import urllib
import urllib2
import os
import oauth2 as oauth
import json
from pymongo import MongoClient
import re

from bs4 import BeautifulSoup
url_first='http://search.dcinside.com/post/p/'
url_second='/q/.EB.A1.9C.EC.8A.A4.ED.8A.B8.20.EC.95.84.ED.81.AC'
headers = {'User-Agent' : 'Mozilla 5.0'}


# 1. key

def getApiKey(keyPath):
    d=dict()
    f=open(keyPath,'r')
    for line in f.readlines():
        row=line.split('=')
        key=row[0]
        d[key]=row[1].strip()
    return d

keyPath="C:\\Users\\Y\\Code\\s_201511138\\src\\twitter4j.properties"
key=getApiKey(keyPath)

# 2. oauth client
consumer = oauth.Consumer(key=key['CONSUMERKEY'], secret=key['CONSUMERSECRET'])
token=oauth.Token(key=key['ACCESSTOKEN'], secret=key['ACCESSTOKENSECRET'])
client = oauth.Client(consumer, token)

# 3. pymongo
from pymongo import MongoClient
Client = MongoClient('localhost:27017')
_db=Client.lostArkCrawl
_collection=_db.crawling

# Oauth설정
url = "https://api.twitter.com/1.1/search/tweets.json"
myparam={'q':'로스트 아크','count':100}
mybody=urllib.urlencode(myparam)
response, content = client.request(url+"?"+mybody, method="GET")

print "다음 해 신작 로스트 아크는 과연 흥할 수 있을까?"
while True:
    print "---------------------------------------------------"
    print "   1. 크롤링 - 처음에 한번만 실행해주세요"
    print "   2. 키워드 분석"
    print "   3. 최근 트위터 데이터 열람"
    print "   4. 트위터 크롤링 - 3,4일에 한번씩 해주세요."
    print "   0. 프로그램 종료"
    print "---------------------------------------------------"
    menu=input("메뉴 선택: ")
    if menu==1:
        #crawling()
        #twitter
        tsearch_json=json.loads(content)
        for tweet in tsearch_json['statuses']:
            #_collection.update_one({"id":tweet['id']},{'$set':{"user":tweet['user'],"text":tweet['text'],"create_at":tweet['created_at']}},True)
            _collection.insert_one(tweet)
            
        #dcinside
        for i in range(1,101):
            url=url_first+str(i)+url_second
            #url='http://search.dcinside.com/post/p/1/q/.EB.A1.9C.EC.8A.A4.ED.8A.B8.20.EC.95.84.ED.81.AC'
            request = urllib2.Request(url, None, headers)
            response = urllib2.urlopen(request)
            html = response.read()
            soup=BeautifulSoup(html,"lxml")
            ptags=soup(class_="des_txt")
            if i%10.0==0:
                print '0',
            for j,tag in enumerate(ptags):
                #print i,tag.text.strip()
                _collection.insert_one({"dc_id":j,"text":tag.text})
        print "\n"
        print "크롤링이 완료되었습니다."
    
    elif menu==2:
        #analysis()
        
        positive_words=['갓겜','언제','빨리 나.*','(나와야.*)','재밌다','(재미.*)','나와라','(기다.*)', '로스트\s?아크\s?하고\s?싶다']
        negetive_words=['지랄','ㅅㅂ','(헬.*)','(망.*)','(죽.*)','내가 개다','병맛','병신','좆','개쓰레기','씨발']
        
        pores=dict()
        neres=dict()

        total=0
        for r in _collection.find():
            data=(r['text']).encode('utf-8')
            total+=1
            for item in positive_words: #긍정어 파싱
                p=re.compile(item)
                m=re.search(p,data)
                if m:
                    if item not in pores.keys():
                        pores[item]=1
                    else:
                        pores[item]+=1
            for nitem in negetive_words: #부정어 파싱
                n=re.compile(nitem)
                m=re.search(n,data)
                if m:
                    if nitem not in neres.keys():
                        neres[nitem]=1
                    else:
                        neres[nitem]+=1

        #단어 숫자 계산
        total_positive=0
        for p in pores.values():
            total_positive+=p

        total_negetive=0
        for n in neres.values():
            total_negetive+=n


        #분석 결과 출력
        positive_percent=float(total_positive)/total*100
        negetive_percent= float(total_negetive)/total*100
        if  positive_percent>negetive_percent:
            winner="축하드립니다. 분석결과 긍정적인 여론이 우세하여, 흥행가능성이 높은 것으로 판명됐습니다.\n"
        else:
            winner="분석결과 안타깝게도 부정적인 여론이 우세하여 흥행가능성이 낮은 것으로  판명됐습니다.\n"
        print "---------------------------------------------------"
        print "분석결과가 나왔습니다."
        print  "총 데이터 수 : ",total
        print "긍정적인 데이터 수: ",total_positive
        print "부정적인 데이터 수: ",total_negetive
        print "\n"
        print "게임 '로스트아크'에 대해 긍정적인 여론이 ",positive_percent,"%, 부정적인 여론이 ", negetive_percent,"%로\n",winner
        print "---------------------------------------------------"
        print "분석결과를 analysis_output.txt 로 저장합니다."
        f=open("./analysis_output.txt",'w')
        fd="분석결과가 나왔습니다.\n 총데이터수: {0}\n 긍정적인 데이터 수: {1}\n 부정적인 데이터 수: {2}\n\n 게임 '로스트 아크'에 대해 긍정적인 여론이 {3}%, 부정적인 여론이 {4}%,임으로 {5}"
        f.write(fd.format(total, total_positive, total_negetive, positive_percent, negetive_percent, winner))
        f.close()
        print "저장되었습니다."
    elif menu==3:
        tsearch_json=json.loads(content)
        for i,tweet in enumerate(tsearch_json['statuses']):
            data=(tweet['text']).encode('utf-8')
            print i,data
    elif menu==4:
         #twitter
        tsearch_json=json.loads(content)
        for tweet in tsearch_json['statuses']:
            #_collection.update_one({"id":tweet['id']},{'$set':{"user":tweet['user'],"text":tweet['text'],"create_at":tweet['created_at']}},True)
            _collection.insert_one(tweet)
        print "크롤링이 끝났습니다."
        
    elif menu==0:
        print "프로그램을 종료합니다"
        break