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