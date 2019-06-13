import base64
import requests
import configparser
import psycopg2
import time
import ciso8601
from datetime import datetime
from dateutil.parser import parse
from sql_queries import *

# configparser
config = configparser.ConfigParser()
config.read_file(open("config/config.cfg"))

client_key = config['TWITTER']['CLIENT_KEY']
client_secret = config['TWITTER']['CLIENT_SECRET']
access_token_key = config['TWITTER']['ACCESS_TOKEN_KEY']
access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']


def authorization_token():

    # key and b64 encoded for twitter token
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_enconded_key = base64.b64encode(key_secret)
    b64_enconded_key = b64_enconded_key.decode('ascii')

    # base url for oauth2
    base_url = "https://api.twitter.com/"
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': "Basic {}".format(b64_enconded_key),
        'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    # auth
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    # auth_resp.status_code -> print 200

    # access_token = access_token, token_type = bearer token
    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return search_headers


def last_tweet(cur, conn):

    cur.execute(tweets_alert_select)
    id_tweet = cur.fetchone()
    conn.commit()

    return id_tweet[0]


def tweets_request(cur, conn, authorization, search_parameters):

    search_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    search_resp = requests.get(search_url, headers=authorization, params=search_parameters)

    tweet_data = search_resp.json()

    len_data = len(tweet_data)

    if len_data > 0:

        print("Inserting {} values into tweets_alert table\n".format(len_data))

        for tweet in tweet_data:

            date = parse(tweet['created_at'])
            timestamp = time.mktime(date.timetuple())
            text = tweet['text'].encode('utf-8')

            tweet_data = (timestamp, date, date.year, date.month, date.day, tweet['id_str'], text)

            try:
                cur.execute(tweets_alert_insert, tweet_data)
            except ValueError as e:
                print(e)

        print("Finished")
        conn.commit()
    else:
        print("\nThere's no new tweets to insert")


def main():
    conn = psycopg2.connect(
        "host=104.198.175.246 dbname=njtransit user=postgres password=yssKdiFqqsGcPFfN")
    cur = conn.cursor()

    # searching for last tweet id in dabatase
    id_last_tweet = last_tweet(cur, conn)

    # seach parameters for tweets using last tweet id. This will works to not duplicate data
    search_parameters = {
        'screen_name': 'NJTRANSIT_NEC',
        'since_id': id_last_tweet,
        'count': 200,
        'include_rts': False
    }

    tweets_request(cur, conn, authorization_token(), search_parameters)
    conn.close()


if __name__ == '__main__':
    main()
