import json
from flask import Flask, request, jsonify
from patreon.fetch_post import fetch_posts
from twitter.post_to_twitter import post_to_twitter
from discord.post_to_discord import post_to_discord
from src.create_message import create_message
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Load the message template from the JSON file
def load_message_template():
    with open('src/message_template.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Main function handler for local Flask server
@app.route('/main', methods=['POST'])
def main():
    try:
        logging.info("Function triggered.")

        # Fetch posts from Patreon
        same_day_posts = fetch_posts()
        if same_day_posts:
            logging.info(f"Fetched posts: {same_day_posts}")

            # Load the message template
            json_template = load_message_template()

            # Generate messages for Twitter and Discord
            message_twitter = create_message(json_template, same_day_posts, "twitter")
            message_discord = create_message(json_template, same_day_posts, "discord")

            # Post the messages
            post_to_twitter(message_twitter)
            post_to_discord(message_discord)

            # Log success
            logging.info(f"Posted to Twitter: {message_twitter}")
            logging.info(f"Posted to Discord: {message_discord}")
            
            # Return a success response
            return jsonify({"message": "Posts published successfully"}), 200
        else:
            logging.info("No new posts today.")
            return jsonify({"message": "No new posts today"}), 200
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run Flask locally
# if __name__ == '__main__':
#     app.run(debug=True)
