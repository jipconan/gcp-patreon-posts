def create_message(json_template, posts, platform=""):
    # Patreon main URL
    base_url = "https://www.patreon.com"

    # Color-to-heart mapping
    color_to_emoji = {
        "red": "❤️",
        "blue": "💙",
        "green": "💚",
        "yellow": "💛",
        "purple": "💜",
        "orange": "🧡",
        "black": "🖤",
        "white": "🤍",
        "pink": "💕",
        "brown": "🤎"
    }

    # Create empty message
    message = ""

    # Tag everyone only for Discord
    if platform == "discord":
        message += json_template['tagEveryone']

    # Header Start
    message += json_template['headerStart']

    # Add one or two titles in the header
    titles = ""
    if len(posts) > 1:
        titles = f"{posts[0]['title']} and {posts[1]['title']}"
    elif len(posts) == 1:
        titles = posts[0]['title']
    message += titles
    
    # Header End
    message += json_template['headerEnd']
    
    # Message, title: url
    for post in posts[:2]:  
        # Collect all matching colors
        hearts = []
        for color, emoji in color_to_emoji.items():
            if color.lower() in post['title'].lower():
                hearts.append(emoji)

        # Join all detected hearts, or leave empty if none
        heart_emojis = " ".join(hearts)

        # Add title and URL with or without hearts
        message += f"{heart_emojis} {post['title']}:\n🔗 {base_url}{post['url']}\n\n"
    
    # Footer
    message += json_template['footer']

    # Add hashtags only if platform is Twitter
    if platform == "twitter":
        message += json_template['hashtags']

    return message
