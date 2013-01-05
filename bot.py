#!/usr/bin/python
# coding: utf-8

import tweepy
import sys
import time
import random
import threading

debug = True

ConsumerKey    = 'vcW8YNiBaHZkBFyR0M26g'
ConsumerSecret = 'AO0s6QwnIo5KXfgAq4I85fU6aGv6xvZDd22SjAoRQFw'
waitTime = 3600
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
mutex = threading.Lock()
	
if debug:
	AccessKey = '1061750402-I0GQOEIQpLIE8A2KxYF8F3eiW8hgRNsV9hqzmVy'
	AccessSecret = 'vZevQ762Hq7OEA05ELE6GUmJiaukkuKEs3E32AL7OM'
	auth.set_access_token(AccessKey, AccessSecret)
else:
	token = GetAccessToken() 
	auth.set_access_token(token.key, token.secret)

api = tweepy.API(auth)


def GetAccessToken():
	print 'Open this URL in browser and grand access: ' + auth.get_authorization_url()
	pin = raw_input('PIN: ').strip()
	auth.get_access_token(pin)
	return auth.access_token

def ReportAboutPutilBalls():
	leftBall = False
	while True:
		if leftBall == 0:
			ball = u'левое'
		else:
			ball = u'правое'
		tweet = u'У Путина зачесалось ' + ball + u' яйцо! ' + str(random.randint(0, 10000000000))
		try:
			mutex.acquire()	
			api.update_status(tweet)
			mutex.release()
			leftBall = not leftBall
			print 'New tweet: ' + tweet
			time.sleep(waitTime) # Wait 1 hour before tweeting again
		except  tweepy.error.TweepError as e:
			mutex.release()
			print e.reason
			time.sleep(waitTime) # Something went wrong. Wait an hour and retry

def FollowUser(user):
	print 'Trying to follow @' + user.screen_name
	try:
		mutex.acquire()
		user.follow()
		mutex.release()
		time.sleep(5) #Wait 5 seconds before following new user
		return True
	except tweepy.error.TweepError as e:
		mutex.release()
		print 'Failed to follow @' + user.screen_name + ' because: ' + e.reason
	return False


def FollowEveryOne(user, level = 0):
	print 'Following followers of @' + user.screen_name + ' at level ' + str(level)
	followedPeopleCount = 0
	if level > 5:
		return
	while True:
		if followedPeopleCount < 1000:
			followedPeopleCount += 1
			try:
				mutex.acquire()
				followers = user.followers()
				mutex.release()
				recursionAcceptableFollowers = []
				for f in followers:
					if FollowUser(f):
						recursionAcceptableFollowers.append(f)
				for f in recursionAcceptableFollowers:
					FollowEveryOne(f, level + 1)
			except tweepy.error.TweepError as e:
				print e.reason
		else:
			mutex.release()
			print "Lets wait 24 hours..."
			time.sleep(waitTime * 24) # Twitter limit :(
			print "Continuing"

tweetThread = threading.Thread(target = ReportAboutPutilBalls)
followThread = threading.Thread(target = FollowEveryOne, 	args=(api.me(), 0))

tweetThread.start()
followThread.start()

print 'Waiting for finish'
for t in threading.enumerate():
	if t is not threading.currendThread():
		t.join()
