import base64
import requests
import configparser

# configparser
config = configparser.ConfigParser()
config.read_file(open("config/config.cfg"))

client_key = config['TWITTER']['CLIENT_KEY']
client_secret = config['TWITTER']['CLIENT_SECRET']
access_token_key = config['TWITTER']['ACCESS_TOKEN_KEY']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_enconded_key = base64.b64encode(key_secret)
b64_enconded_key = b64_enconded_key.decode('ascii')

base_url = "https://api.twitter.com/"
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': "Basic {}".format(b64_enconded_key),
    'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}


auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
# auth_resp.status_code -> print 200

# access_token = access_token, token_type = bearer token
access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

search_parameters = {
    'screen_name': 'NJTRANSIT_NEC',
    'count': 100,
    'include_rts': False
}

search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_parameters)

print(search_resp.status_code)

tweet_data = search_resp.json()

for tweet in tweet_data:
    date = tweet['created_at']
    text = tweet['text']
    try:
        print("Created at: {} \n Tweet: {}".format(str(date), str(text.encode('utf-8'))))
    except ValueError as e:
        print(e)
