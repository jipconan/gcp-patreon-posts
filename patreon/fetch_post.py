from datetime import datetime, timedelta, timezone
import requests
import os
from dotenv import load_dotenv

load_dotenv("patreon/.env")

# Singapore time zone offset
SINGAPORE_TZ = timezone(timedelta(hours=8))

# Function to fetch today's posts from Patreon
def fetch_posts(period=datetime.now(SINGAPORE_TZ).date()):
    access_token = os.getenv("PATRON_API_KEY")
    campaign_id = os.getenv("PATRON_CAMPAIGN_ID")
    # print("access_token:", access_token)

    # Make an API call to get today's posts
    response = requests.get(
        f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts?page%5Bcount%5D=10&sort=-published_at",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"fields[post]": "title,content,published_at,url"}
    )
    while "next" in response.json().get('links', []):
        response = requests.get(
        response.json().get('links', [])["next"],
        headers={"Authorization": f"Bearer {access_token}"},
        params={"fields[post]": "title,content,published_at,url"}
    )

    # Log Singapore Date Time
    # print("Period date (Singapore Time):", period)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch posts: {response.content}")

    posts = response.json().get('data', [])

    print(response.json().get('links', []))
    print(posts[0]['attributes']['published_at'])
    # Filter posts published today and extract necessary fields
    today_posts = []
    for post in posts:
        published_at_utc = post['attributes']['published_at']
        # Parse the UTC time
        published_at = datetime.fromisoformat(published_at_utc).replace(tzinfo=timezone.utc)
        # Convert to Singapore time
        published_at_sg = published_at.astimezone(SINGAPORE_TZ).date()
        
        # Log the publish date in Singapore time
        # print("Post Publish Date (Singapore Time):", published_at_sg)
        
        # Check if the post was published today in Singapore time
        if published_at_sg == period:
            today_posts.append({
                'title': post['attributes'].get('title'),
                'content': post['attributes'].get('content'),
                'url': post['attributes'].get('url')
            })
    
    return today_posts