"""
Direct Discord DM sender using a user token.

Loads DISCORD_USER_TOKEN and FRIEND_ID from a .env file located in the same
directory as this script, then sends a hardcoded DM to the target user via
two sequential Discord REST API (v10) calls:

  1. POST /users/@me/channels — opens (or retrieves) the DM channel between
     the authenticated user and FRIEND_ID, returning the channel ID.
  2. POST /channels/{channel_id}/messages — sends the message
     "This is a test from my python script!" into that DM channel.

Unlike the bot scripts, this authenticates as a regular Discord user account
(DISCORD_USER_TOKEN) rather than a bot token.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

token = os.getenv('DISCORD_USER_TOKEN')
user_id = os.getenv('FRIEND_ID')

headers = {"Authorization": token}

response = requests.post(
    "https://discord.com/api/v10/users/@me/channels",
    headers=headers,
    json={"recipient_id": user_id}
)

channel_id = response.json()["id"]
print(channel_id)

requests.post(
    f"https://discord.com/api/v10/channels/{channel_id}/messages",
    headers=headers,
    json={"content": "This is a test from my python script!"}
)