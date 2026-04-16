"""
Discord webhook sender.

Loads a webhook URL from a .env file (DISCORD_WEBHOOK_URL) and immediately
POSTs a single embed message to that webhook using the Discord REST API.

The embed contains a hardcoded title, description, and color (red, 0xFF0000).
The request uses the '?wait=true' query parameter so Discord returns the
created message object in the response body.

On success (HTTP 200) the response JSON is printed; any other status code
prints a 'No content returned' notice instead.
"""
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