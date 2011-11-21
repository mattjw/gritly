import tweepy, re, json
from geopy import geocoders

# Retrieves postcodes from text
# Only first postcode in the text
def getPostCode(t):
	r = "\s[a-zA-Z]{1,2}[0-9]{1,2}\s?[0-9]{1}[a-zA-Z]{2}"
	m = re.search(r,t)
	if m==None:
		return None
	else:
		return m.group(0).strip()

def getLatLong(postcode):
	g = geocoders.Google()
	code = g.geocode(postcode)
	return code


##########################################################################
#									 #
#				NOW USED				 #
#									 #
##########################################################################

# Finds instances of s in t (case inspecific)
def getString(t, s):
	t_low = t.lower()
	s=s.lower()
	loc = t_low.find(s)
	return t[loc:loc+len(s)]

# removes target from s
def removeFromString(s, target):
	noiseChars = ",.:- "
	if type(target)	== list:
		for t in target:
			tok = getString(s,target)
			parts = s.split(tok, 1)
			s = parts[0].strip(noiseChars)+" "+parts[1].strip(noiseChars)
		result = s
	else:	
		tok = getString(s,target)
		parts = s.split(tok, 1)
		if len(parts)==2:		
			result = parts[0].strip(noiseChars)+" "+parts[1].strip(noiseChars)
		else:
			result = parts[0]
	return result.strip()

##########################################################################
#									 #
#				END OF NOW USED				 #
#									 #
##########################################################################

# Gets tweets from within the UK containing query q.
# Will retrieve all tweets allowed from API
# Shouldn't contain repeated tweets (except retweets)
def searchTweets(q):
	a = tweepy.API()
	more = True
	c=1
	total=0
	done=[]
	result=[]	
	while more==True:
		tweets = a.search(q, locale="United Kingdom", rpp=100, page=c)
		if len(tweets)==0:
			more = False
		else:
			count = 0
			for tweet in tweets:
				if tweet.__dict__['id'] not in done:
					done.append(tweet.__dict__['id'])
					result.append(tweet)
					count+=1
					total+=1
			if count==0:
				more = False
		c+=1
	return result

# Find tweets containing q within loc

def searchTweetsLocation(q, loc):
	a = tweepy.API()
	more = True
	c=1
	total=0
	done=[]
	result=[]
	while more==True:
		tweets = a.search(q, geocode=loc, rpp=100, page=c)
		if len(tweets)==0:
			more = False
		else:
			count = 0
			for tweet in tweets:
				if tweet.__dict__['id'] not in done:
					done.append(tweet.__dict__['id'])
					result.append(tweet)
					count+=1
					total+=1
			if count==0:
				more = False
		c+=1
	return result

# Searches for tweets containing q within which a postcode was found
# returns json containing 'id', 'tweet', 'postcode', 'geo' (Null if not present), 'created_at' (ISO Format YYYY-MM-DDTHH:MM:SS), 'clean' (Tweet with search term and postcode removed), 'postcode_loc' lat/long of postcode found in tweet

def getTweets(q):
	result = []	
	tweets = searchTweets(q)
	for tweet in tweets:
		tweet_id = str(tweet.__dict__['id'])
		author = tweet.__dict__['from_user']
		av_url = tweet.__dict__['profile_image_url']
		text = tweet.text
		postcode = getPostCode(text)
		if not(postcode==None):
			clean = removeFromString(text, q)
			clean = removeFromString(clean, postcode)
			latlong = getLatLong(postcode)[-1]
			result.append({'id':tweet_id,'tweet':text,'postcode':postcode,'geo':tweet.__dict__['geo'], 'created_at':tweet.__dict__['created_at'].isoformat(),'clean':clean, 'postcode_loc':latlong, 'author':author,'avatar_url':av_url})
	return json.dumps(result)

# Searches for tweets containing q within dist of lat, lon
# returns json containing 'id', 'tweet', 'postcode', 'geo' (Null if not present), 'created_at' (ISO Format YYYY-MM-DDTHH:MM:SS), 'clean' (Tweet with search term and postcode removed), 'postcode_loc' lat/long of postcode found in tweet

def getTweetsLocation(q, lat, lon, dist):
	result = []
	loc = str(lat)+","+str(lon)+","+str(dist)	
	tweets = searchTweetsLocation(q, loc)
	for tweet in tweets:
		tweet_id = str(tweet.__dict__['id'])
		author = tweet.__dict__['from_user']
		av_url = tweet.__dict__['profile_image_url']
		text = tweet.text
		postcode = getPostCode(text)
		if not(postcode==None):
			clean = removeFromString(text, q)
			clean = removeFromString(clean, postcode)
			latlong = getLatLong(postcode)[-1]
			result.append({'id':tweet_id,'tweet':text,'postcode':postcode,'geo':tweet.__dict__['geo'], 'created_at':tweet.__dict__['created_at'].isoformat(),'clean':clean, 'postcode_loc':latlong, 'author':author,'avatar_url':av_url})
	return json.dumps(result)
