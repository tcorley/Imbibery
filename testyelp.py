import json
import pprint
import sys
import urllib
import urllib2

import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = '2kUy0Cv_GOZv0EaoKT3g6Q'
CONSUMER_SECRET = 'ORP2p-GgTgjsMWHJRmYPgjCOs8w'
TOKEN = 'WEtBW1O8hxsjM68fs9Mntl_PGxMLLIlh'
TOKEN_SECRET = 'mLeQop35JVdjzDlb8Udc2z87I7I'

url_params = {
    'location': 'Austin,TX',
    'category_filter': 'restaurants',
    'sort': 2,
    'offset':20
}

url = 'http://{0}{1}?'.format(API_HOST, urllib.quote(SEARCH_PATH.encode('utf8')))

consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

oauth_request.update(
    {
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': oauth2.generate_timestamp(),
        'oauth_token': TOKEN,
        'oauth_consumer_key': CONSUMER_KEY
    }
)

token = oauth2.Token(TOKEN, TOKEN_SECRET)
oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
signed_url = oauth_request.to_url()

conn = urllib2.urlopen(signed_url, None)
try:
    response = json.loads(conn.read())
finally:
    conn.close()

print(len(response.get('businesses')))