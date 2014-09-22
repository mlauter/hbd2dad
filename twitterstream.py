import os
import tweepy
import json
from firebase import firebase

firebase_ref = firebase.FirebaseApplication('https://happybirthdaydad.firebaseio.com/', None)

#set up twitter keys

CONSUMER_KEY = os.environ["TWITTER_API_KEY_HBD"]
CONSUMER_SECRET = os.environ["TWITTER_API_SECRET_HBD"]

# just going to use the ones I generated on the site
ACCESS_TOKEN_KEY = os.environ["TWITTER_ACCESS_TOKEN_HBD"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET_HBD"]



TWITTER_STREAM_API_PATH = '/1/statuses/sample.json'

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        
        # print json.dumps(decoded, indent=4)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s\ncoordinates: %s\nusr_loc: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'), decoded['coordinates'], decoded['user']['location'])
        print ''

        coords =  decoded['coordinates']
        if coords:
            self.store_data(coords)

        return True

    def store_data(self, coords):
        coords = coords['coordinates']
        firebase_ref.post('/processed_coords',coords)
        
    def on_error(self, status):
        print status


if __name__ == "__main__":
    l = StdOutListener()

    url = 'https://stream.twitter.com/1.1/statuses/filter.json?delimited=length&track=twitterapi&'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    stream = tweepy.Stream(auth, l)
    stream.filter(track=['happybirthday','happy birthday', 'feliz cumpleanos', 'felizcumpleanos', 'joyeux anniversaire', 'joyeuxanniversaire'])





