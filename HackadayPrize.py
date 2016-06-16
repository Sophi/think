import tweepy, time, sys, json, os, random
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from multiprocessing import Pool #run multi threads at once

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
start_time = time.time() #grabs the system time
our_own_id = 'HackadayPrize'

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):      
        all_data = json.loads(data)
        username = all_data["user"]["screen_name"]
        timeStamp = all_data["timestamp_ms"] #unixtime
        doTweet = all_data["id"]
        lastTime = timeStamp
        if username != our_own_id:
            print(username) # just so we know it's working
        try:
            sleepTime = random.randrange(30, 100, 2)  #RT at diff times
            print(sleepTime)
            time.sleep(sleepTime) #seconds
            api.retweet(doTweet)
        except tweepy.TweepError as errorCode:
            print(errorCode)
        return True
    
    def on_error(self, status_code): #Tweepy’s Stream Listener passes error messages to on_error stub 
       if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        
    def on_status(self, status): #on_data passes data from statuses to on_status 
        print(status.text)
        
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
    
def main():
    listener = StdOutListener() 
    stream = tweepy.Stream(auth, listener)
    
    print ("Streaming started...")

    try:
      stream.filter(track=['#HackadayPrize','HackadayIO'])        
    except KeyboardInterrupt:
       sys.exit()

if __name__ == '__main__':
    main()
    print("I crashed here")
 
   
