import requests
import os
from dotenv import load_dotenv

load_dotenv("discord/.env")

# Function to post a message to Discord
def post_to_discord(message):
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    discord_api_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    bot_token = os.getenv("DISCORD_BOT_TOKEN")

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    payload = {"content": message}

    response = requests.post(discord_api_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to post to Discord: {response.content}")