# Lambda Patreon Integration

## Overview

This project is a serverless application that automatically retrieves and shares the latest posts from a Patreon campaign on Twitter and Discord. It’s built using AWS Lambda triggered by CloudWatch event. By integrating with the Patreon API, Twitter API, and Discord API, the application automates the process of sharing new campaign posts with followers across platforms.

## Functionality

The application performs several key functions:

1. **Fetch Patreon Posts**  
   The application uses the Patreon API to retrieve recent posts from a specified campaign. It filters posts based on the current date to identify and prepare only the most recent updates for sharing.

2. **Create a Formatted Message**  
   Once new posts are identified, they are combined into a single, formatted message. This message includes post titles and URLs, as well as predefined text and emojis to maintain consistency and engagement across platforms.

3. **Post to Twitter and Discord**

   - **Twitter**: The function authenticates with Twitter’s API using OAuth 1.0a and posts the formatted message as a tweet.
   - **Discord**: Using the Discord Bot API, the function posts the same message to a designated Discord channel, notifying followers of the latest updates.

4. **Error Handling and Logging**  
   Errors encountered during API calls (e.g., failed authentication or posting issues) are logged to AWS CloudWatch, providing traceability and supporting troubleshooting.

## Usage

This Lambda function is triggered on a set schedule, capturing the latest campaign content daily. Users can customize the posting schedule by updating the configuration in the AWS console.

---
