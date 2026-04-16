"""
One-shot Discord DM sender.

Loads DISCORD_TOKEN and DISCORD_USER_ID from a .env file, then starts a
minimal Discord bot that does the following as soon as it connects:

  1. Fetches the user object for the configured DISCORD_USER_ID.
  2. Sends that user a hardcoded test DM ("This is a test message from my
     Discord bot!").
  3. Immediately shuts the bot down (bot.close()).

The bot uses default intents (no privileged intents required) and exits after
sending the single message, making this a fire-and-forget utility script.
"""
import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
print(os.getenv('DISCORD_USER_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
token = os.getenv('DISCORD_TOKEN')
discord_user_id = int(os.getenv('DISCORD_USER_ID'))

@bot.event
async def on_ready():
    user = await bot.fetch_user(discord_user_id)
    await user.send("This is a test message from my Discord bot!")
    await bot.close()

bot.run(token)