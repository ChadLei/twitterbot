import tweepy
import time
from playsound import playsound
from multiprocessing import Process

ChadLe14_consumer_key = 'sy1wATwFxDoetQFPFc1IMJuFh'
ChadLe14_consumer_secret = 'KjRrldyr03VN2iDKpMk905AYhZdBG8eHGV8dZDpPrQvTwZX28s'
ChadLe14_access_token = '1153774025711030273-zdqneNw0Epe8Sl8Wge7CZl2jqYpvTH'
ChadLe14_access_token_secret = 'x1Wdl35xJjzBUXpiSuWU7lPwGBz2k2LanCcmwlmp2rhqs'

chadeezy1_consumer_key = 'PYi16RrC0RRhMiHafCGWMM7yo'
chadeezy1_consumer_secret = 'PNweozp92bsbmeZ903EncMbvu9Mc8EyO8SSPbViLCT4vGo22Lx'
chadeezy1_access_token = '1155186458468085760-UD0JsKKC7X215Zm0qcLUkJUzf2xZum'
chadeezy1_access_token_secret = 'JXrdPHpP2c138BxvlhiKugRP23QLSYByZH1iPwqJ4ChUJ'

# user = api.me()

def main(name,consumer_key,consumer_secret,access_token,access_token_secret):

	# User-authentication allows for 180 queries per access token every 15 minutes
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Pass our consumer key and consumer secret to Tweepy's user authentication handler
	auth.set_access_token(access_token, access_token_secret) #Pass our access token and access secret to Tweepy's user authentication handler
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Creating a twitter API wrapper using tweepy

	# Switch to application authentication - application-only authentication allows for 450 queries every 15 minutes
	# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret) 
	# api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Setting up new api wrapper, using authentication only

	tweetCount = 0
	# search = ("like", "retweet", "win", "giveaway", "rt to win", "chance to win")
	search = ("win free OR #rttowin OR #giveaway OR giveaway OR like and retweet OR like and rt OR retweet to enter OR retweet to win OR c OR rt to win OR chance to win OR giving away OR win free OR win a free OR chance to win -filter:retweets")
	# search = ("tag")
	numOfTweets = 1000 #Maximum number of tweets we want to collect 
	
	for tweet in tweepy.Cursor(api.search, search, count=100, tweet_mode='extended').items(numOfTweets):
		try:
			print("[USERNAME: " + tweet.user.screen_name + "]")
			tweetText = tweet.full_text
			wackWords = ['follow', 'comment', 'survey', 'fill out', 'reply', 'rsvp', 'enter here', 'click to', 'dm ']
			if  all(word not in tweetText.lower() for word in wackWords):
				print(tweetText.lower())
				if 'like' in tweetText.lower():
					tweet.favorite()
					print("---- [Liked] ----")
				if 'retweet' in tweetText.lower() or 'rt' in tweetText.lower():
					tweet.retweet()
					print("---- [Retweeted] ----")
				if 'tag ' in tweetText.lower() or 'tell us' in tweetText.lower():
					userID = tweet.user.screen_name
					comment = "@%s @officialchidori @chazeechazy @ChadLe14 @chadeezy1 dude check that out lol!! the first one obviously :)" % (userID)
					api.update_status(comment, tweet.id)
					print("---- [Tagged] ----")
				tweetCount += 1
				print("[Number of tweets " + name + " has gone through: " + str(tweetCount) + ']\n')
				time.sleep(100)
				# api.create_friendship(tweet.user.id)
		except tweepy.TweepError as e:
			print('---- Error: '+ str(e[0][0]['message']) + ' ----\n')
			break
			continue
		except StopIteration:
			print("[I have stopped for some reason....]")
			break
		except UnicodeEncodeError:
			print("[(tweetText.lower() couldn't convert tweet....]")
			continue
	# print(api.rate_limit_status()['resources']['search']) #You can check how many queries you have left using rate_limit_status() method
	print("**************** Complete! ****************\n")

# main("ChadLe14",ChadLe14_consumer_key,ChadLe14_consumer_secret,ChadLe14_access_token,ChadLe14_access_token_secret)
# main("chadeezy1",chadeezy1_consumer_key,chadeezy1_consumer_secret,chadeezy1_access_token,chadeezy1_access_token_secret)

if __name__ == '__main__':
	p1 = Process(target=main("ChadLe14",ChadLe14_consumer_key,ChadLe14_consumer_secret,ChadLe14_access_token,ChadLe14_access_token_secret))
	p1.start()
	p2 = Process(target=main("chadeezy1",chadeezy1_consumer_key,chadeezy1_consumer_secret,chadeezy1_access_token,chadeezy1_access_token_secret))
	p2.start()
	p1.join()
	p2.join()

	playsound('drake.mp3')



