
from tweepy import OAuthHandler
import tweepy
import urllib2
import json
from unidecode import unidecode

CKEY = "uGqlRtyQtr9QdfC8lyOxF0mMH"
CSECRET = "OOTmTNdS08ZIiCVzDZY6KK07YgJfiMnkErRwySNNiAbWYkxfGB"
ATOKEN = "2518946128-gxD9hE4tznkkGcbsVeCwpiTCtB0UggISxAW9c8D"
ATOKENSECRET = "5ki7vufqapxhZ6bstoCYIvPtq3KMnREhSeVnO5YnvgSkD"

URL_SENTIMENT140 = "http://www.sentiment140.com/api/bulkClassifyJson"

POLITICIAN = "Trump"
LIMIT = 2500
LANGUAGE = 'es' # Sentiment140 API only support English or Spanish.

def parse_response(json_response):
   negative_tweets, positive_tweets = 0, 0
   for j in json_response["data"]:
       if int(j["polarity"]) == 0:
           negative_tweets += 1
       elif int(j["polarity"]) == 4:
           positive_tweets += 1
   return negative_tweets, positive_tweets

def main():
   auth = OAuthHandler(CKEY, CSECRET)
   auth.set_access_token(ATOKEN, ATOKENSECRET)
   api = tweepy.API(auth)
   tweets = []

   for tweet in tweepy.Cursor( api.search,
                               q='Raila',
                               result_type='recent',
                               include_entities=True,
                               lang=LANGUAGE).items(LIMIT):
       aux = { "text" : unidecode(tweet.text.replace('"','')), "language": LANGUAGE,  "query" : POLITICIAN, "id" : tweet.id }
       tweets.append(aux)

   result = { "data" : tweets }

   req = urllib2.Request(URL_SENTIMENT140)
   req.add_header('Content-Type', 'application/json')
   response = urllib2.urlopen(req, str(result))
   json_response = json.loads(response.read())
   negative_tweets, positive_tweets = parse_response(json_response)

   print "Positive Tweets: " + str(positive_tweets)
   print "Negative Tweets: " + str(negative_tweets)

if __name__ == '__main__':
   main()
