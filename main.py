import tweepy
import os
import logging

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

logging.basicConfig(filename='log.txt', format= "%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None:
            #if the tweet is a reply, we just fav it
            try:
                tweet.favorite()
                logger.info(f"Liking {tweet.user.name}")
            except:
                logger.error(f"Error on faving a reply by {tweet.user.name}", exc_info=True)

        if tweet.in_reply_to_status_id is None:
            #if it's not a reply, we fav and retweet it
            try:
                tweet.favorite()
                tweet.retweet()
                logger.info(f"Liking & retweeting {tweet.user.name}")
            except:
                logger.error(f"Error on handling a tweet by {tweet.user.name}", exc_info=True)

    def on_error(self, status):
        logger.error("Something went wrong: " + status, exc_info=True)

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:  # check credentials
        api.verify_credentials()
        #print("dobro")
        logger.info("Authenticated correctly")
    except:
        #print("ni dobro")
        logger.exception("Error on authentication")

    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["trenitaliamerda", "italomerda", "trenordmerda"])

if __name__ == "__main__":
    main()