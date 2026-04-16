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