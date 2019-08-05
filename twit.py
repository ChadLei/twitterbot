import tweepy
import time
from playsound import playsound
from multiprocessing import Process
import csv
import re
from sys import argv


# Different keys and tokens for different accounts
ChadLe14_consumer_key = 'sy1wATwFxDoetQFPFc1IMJuFh'
ChadLe14_consumer_secret = 'KjRrldyr03VN2iDKpMk905AYhZdBG8eHGV8dZDpPrQvTwZX28s'
ChadLe14_access_token = '1153774025711030273-zdqneNw0Epe8Sl8Wge7CZl2jqYpvTH'
ChadLe14_access_token_secret = 'x1Wdl35xJjzBUXpiSuWU7lPwGBz2k2LanCcmwlmp2rhqs'

chadeezy1_consumer_key = 'PYi16RrC0RRhMiHafCGWMM7yo'
chadeezy1_consumer_secret = 'PNweozp92bsbmeZ903EncMbvu9Mc8EyO8SSPbViLCT4vGo22Lx'
chadeezy1_access_token = '1155186458468085760-UD0JsKKC7X215Zm0qcLUkJUzf2xZum'
chadeezy1_access_token_secret = 'JXrdPHpP2c138BxvlhiKugRP23QLSYByZH1iPwqJ4ChUJ'

# Searches Twitter for tweets relating to giveaways and fulfills requirements to win baby!
def main(name,consumer_key,consumer_secret,access_token,access_token_secret):
	# User-authentication allows for 180 queries per access token every 15 minutes
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Pass our consumer key and consumer secret to Tweepy's user authentication handler
	auth.set_access_token(access_token, access_token_secret) #Pass our access token and access secret to Tweepy's user authentication handler
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Creating a twitter API wrapper using tweepy

	# Switch to application authentication - application-only authentication allows for 450 queries every 15 minutes
	# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret) 
	# api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #Setting up new api wrapper, using authentication only

	tweetCount = 0 # Count of how many tweets I've gone through so far
	numOfTweets = 3000 # Maximum number of tweets we want to collect 
	numberOfTotalTweetsGoneThru = 0
	# search = ("#rttowin OR #giveaway OR (give away) OR giveaway OR (likes and rts) OR (like and retweet) OR (like and rt) OR (retweet to enter) OR (retweet to win) OR (rt to win) OR (chance to win) OR (giving away) OR (win free) OR (win a free) OR (chance to win) -filter:retweets")
	search = ('''
		((likes and rts) OR 
		(like and retweet) OR 
		(like and rt)) AND 

		(a lifetime copy of) OR
		(win a copy of) OR
		(win a lifetime) OR 
		(retweet to enter) OR 
		(retweet to win) OR 
		(rt to win) OR 
		(chance to win) OR
		(give away) OR 
		(giveaway) OR 
		(#giveaway) OR 
		(giving away) OR
		(#rttowin) OR 
		(win free) OR 
		(win a free)  
		-filter:retweets''')

	# Words to ignore since these actions are too specific at the moment
	wackWords = ['pass royale','V-Bucks','follow whoever','retweet with the tag','ping account','Adoptme','answer the poll','instagram','facebook','cash',
		'sign up','code','$','bounty reward','coin','give proof','show proof','stream','streamer','staxel','fortnite','twitch', 'survey', 'fill out', 'rsvp', 
		'enter here','click to','dm ','battle pass','battlepass','win nothing','help me','#sugar','ikonik bundles','discount 30%','discount 50%','send me a picture',
		'send me a', 'knight ranks'
	] 
			
	for tweet in tweepy.Cursor(api.search, search, count=100, tweet_mode='extended').items(numOfTweets):
		numberOfTotalTweetsGoneThru += 1
		try:
			# Avoids a account called Bot Spotting that is used to catch bots
			if tweet.user.name == 'Bot Spotting' or 'bot' in tweet.user.name.lower(): 
				continue

			# Checks tweets for what the user wants us to do in order to be eligible for the giveaway and executes certain actions
			tweetText = tweet.full_text
			if  all(word not in tweetText.lower() for word in wackWords):
				# Keeps track of users that this script has gone through to check for specific accounts (sneaker bot related accounts)
				print("[USERNAME: " + tweet.user.screen_name + "]")
				# with open('usersIWentThrough.csv', 'a') as data_file:
				# 	writer = csv.writer(data_file)
				# 	writer.writerow([tweet.user.screen_name])

				# Checks criteria and acts accordingly
				print(tweetText.lower())
				if 'like' in tweetText.lower():
					tweet.favorite()
					print("---- [Liked] ----")
				if 'retweet' in tweetText.lower() or 'rt' in tweetText.lower():
					tweet.retweet()
					print("---- [Retweeted] ----")
				if 'tag ' in tweetText.lower() or 'tell us' in tweetText.lower() or 'comment' in tweetText.lower() or 'reply' in tweetText.lower():
					userID = tweet.user.screen_name
					comment = "@%s @officialchidori @chazeechazy @ChadLe14 @chadeezy1 i'm done, look yall i dig this im bettin sz 10 US  :)" % (userID)
					api.update_status(comment, tweet.id)
					print("---- [Tagged] ----")
				if 'follow' in tweetText.lower():
					api.create_friendship(tweet.user.id)
					print("---- [Followed: @" + tweet.user.screen_name + "] ----")
					textlist = re.split('[,\s\n]',tweetText.lower())
					for subtext in textlist:
						if subtext.startswith('@'):
							try:
								person = subtext.strip('@').strip(',').strip('\n').strip('!') 
								personID = api.get_user(person).id # Retrieves user's ID so that Twitter can follow them
								api.create_friendship(personID)
								print("---- [Followed: @" + person + "] ----")
							except:
								print("---- [Couldn't follow: " + subtext + "] ----") # Catches errors when Twitter cannot find specified user to follow
				tweetCount += 1
				print("[Number of tweets " + name + " has gone through: " + str(tweetCount) + ']\n')
				time.sleep(100)
			else:
				# print(tweetText.lower())
				print("---- [Skipped user " + tweet.user.screen_name + " - probably due to tweet containing a wack word] ----\n")
				# time.sleep(5)
		except tweepy.TweepError as e:
			# print('---- Error: '+ str(e[0][0]['message']) + ' ----\n')
			print('---- Error: '+ str(e) + ' ----\n')
			continue
		except StopIteration:
			print("[I have stopped for some reason....]")
			break
		except UnicodeEncodeError:
			print("[(tweetText.lower() couldn't convert tweet....]")
			continue
	# print(api.rate_limit_status()['resources']['search']) #You can check how many queries you have left using rate_limit_status() method
	# print("[Number of tweets has gone through: " + str(tweetCount) + ']\n')
	print("**************** Complete! ****************")
	print("[Number of tweets liked/retweeted/followed: " + str(tweetCount) + ']\n')
	print("**************** Total number of tweets gone thru: " + str(numberOfTotalTweetsGoneThru) + ' ****************\n')

 







def startProcess():
	p1 = Process(target=main("ChadLe14",ChadLe14_consumer_key,ChadLe14_consumer_secret,ChadLe14_access_token,ChadLe14_access_token_secret))
	p1.start()
	p2 = Process(target=main("chadeezy1",chadeezy1_consumer_key,chadeezy1_consumer_secret,chadeezy1_access_token,chadeezy1_access_token_secret))
	p2.start()
	p1.join()
	p2.join()




if __name__ == '__main__':
	name = argv[1]
	consumer_key = argv[2]
	consumer_secret = argv[3]
	access_token = argv[4]
	access_token_secret = argv[5]
	main(name,consumer_key,consumer_secret,access_token,access_token_secret)
	# main("ChadLe14",ChadLe14_consumer_key,ChadLe14_consumer_secret,ChadLe14_access_token,ChadLe14_access_token_secret)
	# main("chadeezy1",chadeezy1_consumer_key,chadeezy1_consumer_secret,chadeezy1_access_token,chadeezy1_access_token_secret)
	# startProcess()
	

	# playsound('drake.mp3')


# python twit.py "ChadLe14" 'sy1wATwFxDoetQFPFc1IMJuFh' 'KjRrldyr03VN2iDKpMk905AYhZdBG8eHGV8dZDpPrQvTwZX28s' '1153774025711030273-zdqneNw0Epe8Sl8Wge7CZl2jqYpvTH' 'x1Wdl35xJjzBUXpiSuWU7lPwGBz2k2LanCcmwlmp2rhqs'
# python twit.py "chadeezy1" 'PYi16RrC0RRhMiHafCGWMM7yo' 'PNweozp92bsbmeZ903EncMbvu9Mc8EyO8SSPbViLCT4vGo22Lx' '1155186458468085760-UD0JsKKC7X215Zm0qcLUkJUzf2xZum' 'JXrdPHpP2c138BxvlhiKugRP23QLSYByZH1iPwqJ4ChUJ'
