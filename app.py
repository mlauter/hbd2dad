from flask import Flask, render_template
import os
import tweepy
import requests
import time
import json

app = Flask(__name__, static_url_path='')

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

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s, %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'), decoded['coordinates'])
        print ''
        return True

    def on_error(self, status):
        print status

@app.route('/', methods=['GET'])
@app.route('/hello_maps', methods=['GET'])
def homepage():
    return render_template('hello_maps.html', key=os.environ["GOOGLE_MAPS_API_KEY"])




if __name__ == "__main__":
    l = StdOutListener()

    url = 'https://stream.twitter.com/1.1/statuses/filter.json?delimited=length&track=twitterapi&'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    stream = tweepy.Stream(auth, l)
    stream.filter(track=['happybirthday'])


    # app.run(debug=True)



