import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('DISCORD_WEBHOOK_URL')
payload = {
    "embeds": [
        {
            "title": "Some Title",
            "description": "Some description here",
            "color": 16711680
        }
    ]
}
response = requests.post(url + "?wait=true", json=payload)
print(response.status_code)

if response.status_code == 200:
    print(response.json())
else:
    print("No content returned")