import tweepy
import botornot
from decimal import *
import csv
import sys
import urlextractor
import os
import json
import urllib2

#Avail customer_key, consumer_secret, access_token, access_token_secret. Create a dictionary named "cfg" having these values
"""
cfg = { 
    "consumer_key"        : 
    "consumer_secret"     : 
    "access_token"        : 
    "access_token_secret" : 
   }
"""


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)


def check_for_bots(check_list):
  
  length = len(check_list)
  counter = 0 # Maintain a counter for number of successive tweets having a time difference less than 10 seconds

  for i in range(0,length -1):

     difference = check_list[(length -1) - (i+1)][1] - check_list[(length -1) - i][1]
    
     #print "Seconds:", difference.total_seconds()
     
     if (int(difference.total_seconds()) < 5):
         counter+=1
  return counter

def get_place(tweet):
	#print type(tweet.place)

	if isinstance(tweet.place, type(None)):
		#print "Location not traceable"
		x = 2	
	else:
		print "This tweet is from: ", tweet.place.country, "and city ", tweet.place.full_name , " and is in language: ", tweet.lang
		print "Co-ordinates ", tweet.place.bounding_box.coordinates
		

def get_all_tweets(screen_name):
  auth = tweepy.OAuthHandler("laqkbHrYXN6r8HSipI6xNKCWP", "HLBxNVpW4v5ahLIMRqVuaPchMlKXUhZgCcIemJal0D39SjuWjI")
  auth.set_access_token("797589780599083008-ZMRx3i8Ry9zrbdfkeF3D4v6iPzE3mKD","xeE3HQLhwhQB4IUksHnM86iMMIetA9RCqm8AOncJkDMjb")
  api = tweepy.API(auth)
  alltweets = []
  check_list = []
  check_tup = []
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
  alltweets.extend(new_tweets)
  oldest = alltweets[-1].id - 1
  while len(new_tweets) > 0:
     print "getting tweets before %s" % (oldest)
     new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
     alltweets.extend(new_tweets)
     oldest = alltweets[-1].id - 1
     print "...%s tweets downloaded so far" % (len(alltweets))
  outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
  texts_from_all_tweets = ""
  #print type(tweet.created_at)
  for t in alltweets: # Make a tuple & thereby a list of the attributes of a tweet
        #print screen_name, "'s tweet with ID ", t.id_str,  " has been retweeted ", t.retweet_count , " times"
	get_place(t)
	check_tup = [t.id_str,t.created_at,t.text.encode("utf-8")]
	check_list.append(check_tup)
	text = t.text.encode("utf-8")
	texts_from_all_tweets = texts_from_all_tweets + " " + text
	

	 
  
  # Checking for url's from the text part of all tweets
  #check_for_urls(texts_from_all_tweets)
	
  with open('%s_tweets.csv' % screen_name, 'wb') as f:
     writer = csv.writer(f)
     writer.writerow(["id","created_at","text"])
     writer.writerows(outtweets)
  pass

  check = check_for_bots(check_list) # Send the list we created to a function check_for_bots which checks for the time difference between successive tweets
  print "Number of successive tweets with a time difference less than 1 second:", check
  if check >= 5:
	#print screen_name, " is a bot" # We report that the current entity is a bot if check is greater than 40
	return True , check
  else:
	#print screen_name, " is a human"
	return False , check
	
def check_for_urls(text_complete):
	avail = urlextractor2.parseText(text_complete)
	#print avail
	#print len(avail)
	array = []
	if len(avail) > 0:
		for i in range(0,len(avail)):
			array.append(avail[i][1])
	

		for i in array:
		    data=json.dumps({
			"client": {
			  "clientId":      "Johns_Hopkins_Student",
			  "clientVersion": "1.5.2"
			},
			"threatInfo": {
			  "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING","POTENTIALLY_HARMFUL_APPLICATION","THREAT_TYPE_UNSPECIFIED"],
			  "platformTypes":    ["WINDOWS","LINUX","IOS","OSX","CHROME","ANDROID","ANY_PLATFORM"],
			  "threatEntryTypes": ["URL"],
			  "threatEntries": [
			    {"url": i}
			  ]
			}
		      }
		    )
		    #print type(data)
		    request=urllib2.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyCs4mdWV_5Iu5u3_FMnCu06yPs5Dyw81rQ",data,headers={'content-type':'application/json'})
		    response=urllib2.urlopen(request)
		    page=response.read()
		    l= json.loads(page)
		    if len(l)!=0:
	    		    print "Response:"+page
	
	


def get_skew_rate(current_user,b):
	lenb = len(b)
	if lenb is  0:
			lenb = 1
	if lenb < current_user.followers_count: 
	
		skew_rate = current_user.followers_count/lenb
	else :
		skew_rate = Decimal(current_user.followers_count)/Decimal(lenb)
	return skew_rate	
	
def main():
  api = get_api(cfg) #this is for initializing the Tweepy API.
  bon = botornot.BotOrNot(**cfg) #this is for the botornot API.
  print sys.argv[1]
  stringofhope = "" 	
  if sys.argv[1] == "bot":
	  for friend in tweepy.Cursor(api.friends).items(): #fetching friend's list from Twitter.
		handle = "@" + friend.screen_name
		result = bon.check_account(handle) #calling botornot API.  result is a dictionary.
		if result > 0.48:
			botornot_decision = True
		else:
			botornot_decision = False

		print friend.screen_name + "=" + str(result["score"])	
		print "###############################"
		for key in result["categories"]:
			print key, " = ", result["categories"][key]
			
		print "###############################"
		#print "Printing all tweets now"
		time_decision, value = get_all_tweets(friend.screen_name)
		stringofhope = str(result["score"]) + ":" + str(value) + "\n" 			
		f = open("data","a")		
		f.write(stringofhope)
		f.close()
		return_list = api.friends_ids(screen_name=friend.screen_name)
		print "The number of followers for", friend.screen_name, " are ",  friend.followers_count, " and he is following ", len(return_list)
		skew= get_skew_rate(friend,return_list)
		if skew <= 0.05:
			skew_decision = True
		else:
			skew_decision = False

		print "The skew rate is: ", skew_decision

		print friend.screen_name, " has ", friend.status.retweet_count, " retweets "
		"""if friend.verified != True:
			print friend.screen_name, " is not a verified account by Twitter"
	  	else:
			print friend.screen_name, " is a verified account by Twitter" """
		if ( (skew_decision and time_decision) or (botornot_decision and time_decision) or (skew_decision and botornot_decision)):
	  		print friend.screen_name," is a bot"
		
	  #f = open("data","w")
          #f.write(stringofhope)
          #f.close()  
        

        
  elif sys.argv[1] == "self":

	  current_user = api.me()
	  print "The number of followers for", current_user.screen_name, " are ",  current_user.followers_count
	  
	  return_list = api.friends_ids(screen_name=current_user.screen_name)
	  print "I am following:" , len(return_list)
	  handle = "@" + current_user.screen_name
	  result = bon.check_account(handle)
	  if result > 0.48:
		botornot_decision = True
	  else:
		botornot_decision = False

	  print current_user.screen_name + " = " + str(result["score"])
	  print "###############################"
	  for key in result["categories"]:
			
			print key, " = ", result["categories"][key]
	
	  print "###############################"		
	  print "Printing all tweets now"
	  time_decision, value = get_all_tweets(current_user.screen_name)
	  return_list = api.friends_ids(screen_name=current_user.screen_name)
	  print "The number of followers for", current_user.screen_name, " are ",  current_user.followers_count, " and he is following ", len(return_list)
	  skew= get_skew_rate(current_user,return_list)
	  if skew <= 0.05:
	  	skew_decision = True
	  else:
	  	skew_decision = False

          print "The skew rate is: ", skew_decision

	  
	  
	  print current_user.screen_name, " has ", current_user.status.retweet_count, " retweets"
	  """if current_user.verified != True:
		print current_user.screen_name, " is not a verified account by Twitter"
	  else:
		print current_user.screen_name, " is a verified account by Twitter" """
		
  	  if ( (skew_decision and time_decision) or (botornot_decision and time_decision) or (skew_decision and botornot_decision)):
	  	print current_user.screen_name," is a bot"
		 
		
  

if __name__ == "__main__":
  main()
