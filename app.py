from flask import Flask, render_template
import os
import requests
from requests_oauthlib import OAuth1
import time
import asyncio
import json

app = Flask(__name__, static_url_path='')

#set up twitter keys

CONSUMER_KEY = os.environ["TWITTER_API_KEY_HBD"]
CONSUMER_SECRET = os.environ["TWITTER_API_SECRET_HBD"]

# just going to use the ones I generated on the site
ACCESS_TOKEN_KEY = os.environ["TWITTER_ACCESS_TOKEN_HBD"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET_HBD"]

OAUTH_KEYS = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_key': ACCESS_TOKEN_KEY,
    'access_secret': ACCESS_TOKEN_SECRET
}

TWITTER_REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
TWITTER_AUTHORIZE_URL = 'https://twitter.com/oauth/authorize'
TWITTER_STREAM_API_HOST = 'stream.twitter.com'
TWITTER_STREAM_API_PATH = '/1/statuses/sample.json'


@app.route('/', methods=['GET'])
@app.route('/hello_maps', methods=['GET'])
def homepage():
    return render_template('hello_maps.html', key=os.environ["GOOGLE_MAPS_API_KEY"])

def build_authorization_header(access_token, consumer):
    url = "https://%s%s" % (TWITTER_STREAM_API_HOST, TWITTER_STREAM_API_PATH)
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_token': access_token.key
        'oauth_consumer_key': consumer.key
    }

    # Sign the request.
    # For some messed up reason, we need to specify is_form_encoded to prevent
    # the oauth2 library from setting oauth_body_hash which Twitter doesn't like.
    req = oauth.Request(method="GET", url=url, parameters=params, is_form_encoded=True)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), CONSUMER, access_token)

    # Grab the Authorization header
    header = req.to_header()['Authorization'].encode('utf-8')
    print("Authorization header:")
    print("     header = %s" % header)
    return header


if __name__ == "__main__":
    access_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
    consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])

    # Build Authorization header from the access_token.
    # auth_header = build_authorization_header(access_token, consumer)

    auth = OAuth1(access_token.key, access_token.secret, consumer.key, consumer.secret)

    url = 'https://stream.twitter.com/1.1/statuses/filter.json?delimited=length&track=twitterapi&'

    
    r = requests.get('http://httpbin.org/stream/20', stream=True, auth=auth)

    for line in r.iter_lines():

        # filter out keep-alive new lines
        if line:
            print(json.loads(line))


    app.run(debug=True)



