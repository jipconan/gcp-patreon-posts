from datetime import datetime, timedelta, timezone
import requests
import os
from dotenv import load_dotenv

load_dotenv("patreon/.env")

# Singapore time zone offset
SINGAPORE_TZ = timezone(timedelta(hours=8))

# Function to fetch posts from Patreon
def fetch_posts(days):
    # Load the access token and campaign ID from the environment variables
    access_token = os.getenv("PATRON_API_KEY")
    campaign_id = os.getenv("PATRON_CAMPAIGN_ID")

    # Define the date range for the past 3 days
    today = datetime.now(SINGAPORE_TZ).date()
    days_ago = today - timedelta(days)

    # Initial API call to get the first page of posts
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts?page%5Bcount%5D=10&sort=-published_at"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"fields[post]": "title,content,published_at,url"}

    posts = []  # To store all posts

    while url:
        response = requests.get(url, headers=headers, params=params)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to fetch posts: {response.content}")

        # Add current page's posts to the list
        data = response.json()
        posts.extend(data.get('data', []))
        
        # Get the next page link, if available
        url = data.get('links', {}).get('next', None)

    # Filter posts published within the specified date range
    fetched_posts = []

    for post in posts:
        # Get the published date in UTC
        published_at_utc = post['attributes']['published_at']
        # Parse the UTC time
        published_at = datetime.fromisoformat(published_at_utc).replace(tzinfo=timezone.utc)
        # Convert to Singapore time
        published_at_sg = published_at.astimezone(SINGAPORE_TZ).date()
        
        # Check if the post was published within the range
        if days_ago <= published_at_sg <= today:
            fetched_posts.append({
                'title': post['attributes'].get('title'),
                'content': post['attributes'].get('content'),
                'url': post['attributes'].get('url'),
                'published_at': str(published_at_sg)
            })
    
    return fetched_posts
