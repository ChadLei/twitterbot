import tweepy
import time

consumer_key = 'sy1wATwFxDoetQFPFc1IMJuFh'
consumer_secret = 'KjRrldyr03VN2iDKpMk905AYhZdBG8eHGV8dZDpPrQvTwZX28s'
access_token = '1153774025711030273-zdqneNw0Epe8Sl8Wge7CZl2jqYpvTH'
access_token_secret = 'x1Wdl35xJjzBUXpiSuWU7lPwGBz2k2LanCcmwlmp2rhqs'

# User-authentication allows for 180 queries per access token every 15 minutes
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Pass our consumer key and consumer secret to Tweepy's user authentication handler
auth.set_access_token(access_token, access_token_secret) #Pass our access token and access secret to Tweepy's user authentication handler
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Creating a twitter API wrapper using tweepy

# Switch to application authentication - application-only authentication allows for 450 queries every 15 minutes
# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret) 
# api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Setting up new api wrapper, using authentication only

# user = api.me()

def main():
	count = 0
	# search = ("like", "retweet", "win", "giveaway", "rt to win", "chance to win")
	search = ("#rttowin OR #giveaway OR giveaway OR like and retweet OR like and rt OR retweet to enter OR retweet to win OR c OR rt to win OR chance to win OR giving away OR win free OR win a free OR chance to win -filter:retweets")
	# search = ("tag")
	numOfTweets = 1000 #Maximum number of tweets we want to collect 
	for tweet in tweepy.Cursor(api.search, search, count=100, tweet_mode='extended').items(numOfTweets):
		try:
			print("[USERNAME: " + tweet.user.screen_name + "]")
			tweetText = tweet.full_text
			wackWords = ['follow', 'comment', 'survey', 'fill out']
			# print(tweetText)
			if  all(word not in tweetText.lower() for word in wackWords):
				print(tweetText.lower())
				if 'like' in tweetText.lower():
					tweet.favorite()
					print("[Liked]")
				if 'retweet' in tweetText.lower() or 'rt' in tweetText.lower():
					tweet.retweet()
					print("[Retweeted]")
				if 'tag' in tweetText.lower():
					userID = tweet.user.screen_name
					comment = "@%s @officialchidori dude check that out lol!!" % (userID)
					api.update_status(comment, tweet.id)
					print("[Tagged]")
				count += 1
				print("[Number of tweets gone through: " + str(count) + ']\n')
				time.sleep(180)
				# api.create_friendship(tweet.user.id)
			
		except tweepy.TweepError as e:
			print(e.reason + '\n')
			# print("[This has already been liked/retweeted, so moving on....]\n")
			# time.sleep(60)
			continue
		except StopIteration:
			print("[I have stopped for some reason....]")
			break
	# print(api.rate_limit_status()['resources']['search']) #You can check how many queries you have left using rate_limit_status() method
	print("[Complete!]")

main()
