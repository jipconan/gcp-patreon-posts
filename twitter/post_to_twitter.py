from requests_oauthlib import OAuth1Session
import os
from dotenv import load_dotenv

load_dotenv("twitter/.env")

# Function to post a message to Twitter with OAuth 1.0a
def post_to_twitter(message):
    twitter_api_url = "https://api.twitter.com/2/tweets"
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Initialize OAuth1 session
    twitter_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )
    
    # Create payload for the tweet
    payload = {"text": message}
    
    # Make the post request to Twitter API
    response = twitter_session.post(twitter_api_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to post to Twitter: {response.content}")