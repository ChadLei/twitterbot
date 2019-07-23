import tweepy
import time

consumer_key = 'sy1wATwFxDoetQFPFc1IMJuFh'
consumer_secret = 'KjRrldyr03VN2iDKpMk905AYhZdBG8eHGV8dZDpPrQvTwZX28s'
access_token = '1153774025711030273-zdqneNw0Epe8Sl8Wge7CZl2jqYpvTH'
access_token_secret = 'x1Wdl35xJjzBUXpiSuWU7lPwGBz2k2LanCcmwlmp2rhqs'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()


def main():
	count = 0
	# search = ("like", "retweet", "win", "giveaway", "rt to win", "chance to win")
	search = ("like and retweet OR like and rt OR retweet to win OR c OR rt to win OR chance to win OR giving away -filter:retweets")
	numOfTweets = 100
	for tweet in tweepy.Cursor(api.search, search, tweet_mode='extended').items(numOfTweets):
		try:
			# tweet.retweet()
			# print("Retweeted")
			print(tweet.user.screen_name)
			# print(tweet.user.id)
			if 'retweeted_status' in tweet._json:
				# print(tweet._json['retweeted_status']['full_text'])
				retweet_text = 'RT @ ' + api.get_user(tweet.retweeted_status.user.id_str).screen_name
				print(retweet_text)
			else:
				tweetText = tweet.full_text
				wackWords = ['follow', 'Follow', 'FOLLOW', 'comment', 'Comment', 'COMMENT', 'tag', 'Tag', 'TAG', 'survey']
				if  any(word not in tweetText for word in wackWords):
					print(tweetText + '\n')
					if 'like' in tweetText or 'Like' in tweetText or 'LIKE' in tweetText:
						tweet.favorite()
						print("[Liked]")
					if 'retweet' in tweetText or 'Retweet' in tweetText or 'RETWEET' in tweetText or 'rt' in tweetText or 'RT' in tweetText:
						tweet.retweet()
						print("[Retweeted]")
					count += 1
					print("Number of tweets gona through: " + str(count) + '\n')
					time.sleep(120)
					# api.create_friendship(tweet.user.id)
		except tweepy.TweepError as e:
			# print(e.reason)
			print("[I have already liked/retweeted, so moving on....]")
			time.sleep(60)
			continue
		except StopIteration:
			break

main()
