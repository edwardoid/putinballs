#!/usr/bin/python
# coding: utf-8

import tweepy
import sys
import time
import random

ConsumerKey    = 'vcW8YNiBaHZkBFyR0M26g'
ConsumerSecret = 'AO0s6QwnIo5KXfgAq4I85fU6aGv6xvZDd22SjAoRQFw'
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)

def get_access_token():
	print 'Open this URL in browser and grand access: ' + auth.get_authorization_url()
	pin = raw_input('PIN: ').strip()
	auth.get_access_token(pin)
	return auth.access_token

token = get_access_token() 
auth.set_access_token(token.key, token.secret)
api = tweepy.API(auth)

waitTime = 3600
leftBall = False
while True:
	if (leftBall) == 0:
		ball = u'левое'
	else:
		ball = u'правое'
	tweet = u'У Путина зачесалось ' + ball + u' яйцо! ' + str(random.randint(0, 10000000000))
	try:
		api.update_status(tweet)
		leftBall = not leftBall
		print 'New tweet: ' + tweet
		time.sleep(3600) # Wait 1 hour before tweeting again
	except  tweepy.error.TweepError:
		time.sleep(3600) # Something went wrong. Wait an hour and retry
