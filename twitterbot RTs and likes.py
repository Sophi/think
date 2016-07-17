import tweepy, time, sys, json, os, random, datetime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from multiprocessing import Pool #run multi threads at once
from keysHackadayIO import keys #import the keys dict

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
start_time = time.time() #grabs the system time
start_time2 = time.ctime(float(start_time))
our_own_id = 'xxx' #insert your user name, or the user name you want to act on
   
class StdOutListener(tweepy.StreamListener):
    def on_data (self, data):
        all_data = json.loads(data)
        username = all_data["user"]["screen_name"]
        timeStamp = all_data["timestamp_ms"] #unixtime
        tweetTime = time.time()
        tweetTime2 = time.ctime(float(tweetTime))
        doTweet = all_data["id"]
        try:
              while (username != our_own_id): 
                  print(username) # just so we know it's working
                  print("This is when this tweet was triggered:", tweetTime2)
                  sleepTime = random.randrange(30, 1000, 2)  #RT at diff times                  
                  print("This is how many seconds to wait for RT:", sleepTime)
                  time.sleep(sleepTime) #seconds
                  print("I'm RTing")
                  api.retweet(doTweet)
                  print("I'm liking")
                  api.create_favorite(doTweet)                 
        except tweepy.TweepError as errorCode:
              print(errorCode)
        return True

    def on_error(self, status_code): #Tweepy Str Listener passes error messages to on_error stub 
       if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        
    def on_status(self, status): #on_data passes data from statuses to on_status 
        print(status.text)
        
    def on_timeout(self):
        print('Timeout...')
        return True # keep listening    
    
def main():
    listener = StdOutListener() 
    stream = tweepy.Stream(auth, listener)    
    print (start_time2, "Streaming started...")
    try:
        stream.filter(track=['#electronics','arduino','@arduino'])
        #example tracking. #arduino is != @arduino
    except KeyboardInterrupt:
       sys.exit()

if __name__ == '__main__':
    main()
    print("I crashed here")
