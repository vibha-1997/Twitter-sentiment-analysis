from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import nltk
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
def calctime(a):
    return time.time()-a
count=0
positive=0
negative=0
compound=0
inittime=time.time()
plt.ion()
ckey='cxijGH5V8W20vYKw1PvyQ2jz7'
csecret='rX2nl4iJ1IEUyDlO63R458DA0ExAgxxkhhtr0XfO64WUhyG8Mb'
atoken='838304303202828288-bnZYFUpcAJZdsBEQEm4SoqfGrVw0yjx'
asecret='iz6M5ZHbaCA8iyn1j2QSWPFkjobe5txnjHl7VyWpKkbhI'

class listener(StreamListener):
    
    def on_data(self,data):
        global inittime
        t=int(calctime(inittime))
        all_data = json.loads(data)
        tweet = all_data["text"].encode("utf-8")
        tweet=" ".join(re.findall("[a-zA-Z]+",tweet))
        blob=TextBlob(tweet.strip())

        global positive
        global negative
        global compound
        global count

        count=count+1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity>=0:
                positive=positive+sen.sentiment.polarity
            else:
                negative=negative+sen.sentiment.polarity
        compound=compound+senti
        print count
        print tweet.strip()
        print senti
        print t
        print str(positive)+' '+str(negative)+' '+str(compound)

        plt.axis([0,70,-20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t],[negative],'ro',[t],[compound],'yo')
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True
        
        
        
    def on_error(self,status):
        print status

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream=Stream(auth,listener(count))
twitterStream.filter(track=['BJP'])

