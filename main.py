"""
Discord bot entry point.

Connects to Discord using a token loaded from a .env file and registers the
following behavior:

Events:
  - on_ready:       Logs a confirmation message when the bot comes online.
  - on_member_join: Sends a welcome DM to any new server member.
  - on_message:     Responds to the '!hello' prefix with a mention greeting,
                    then delegates to the command framework.

Commands (prefix '!'):
  - dm <msg>:   Sends the caller a DM echoing their message.
  - reply:      Replies directly to the caller's message with a mention.
  - poll <q>:   Posts an embed with the given question and adds thumbs-up/down
                reactions to act as a simple poll.
  - hello:      Greets the caller in the channel.
  - assign:     Gives the caller the 'Gamer' role if it exists on the server.
  - remove:     Removes the 'Gamer' role from the caller.
  - secret:     Sends a special message exclusively to members who hold the
                'Gamer' role (enforced by @commands.has_role).

All Discord activity is written to discord.log at DEBUG level.
"""
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Gamer"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.name}!')
    print(f'{member} has joined the server!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # if "shit" in message.content.lower():
    #     await message.delete()
    #     await message.channel.send(f'{message.author.mention}, please watch your language!')

    if message.content.startswith('!hello'):
        await message.channel.send(f'Hello, {message.author.mention}!')
    
    await bot.process_commands(message)

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply(f'{ctx.author.mention}, this is a reply to your message!')

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction('👍')
    await poll_message.add_reaction('👎')

@bot.command
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention}, you have been assigned the {secret_role} role!')
    else:
        await ctx.send(f'Sorry, {ctx.author.mention}, the {secret_role} role does not exist.')

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention}, the {secret_role} role has been removed from you!')
    else:
        await ctx.send(f'Sorry, {ctx.author.mention}, the {secret_role} role does not exist.')

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    if any(role.name == secret_role for role in ctx.author.roles):
        await ctx.send(f'Welcome to the secret area, {ctx.author.mention}!')
    else:
        await ctx.send(f'Sorry, {ctx.author.mention}, you do not have access to the secret area.')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)