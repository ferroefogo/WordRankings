# WordRanking Discord Bot
# This bot will take a search query from a user and output the user who has used that word the most and how many times.
# There will be leaderboards of the top people who used the word.

import discord
from discord.ext import commands
import os

my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='!')



@bot.command()
async def keyword(ctx, *, word: str):
  msgCount = 0
  channel = bot.get_channel(559807757427933217)
  messages = await ctx.channel.history(limit=None).flatten()
  for msg in messages:
    if str(msg.author) != "WordRankings#3933":
      msg.content = msg.content.lower()
      if word in msg.content:
        if '!keyword' not in msg.content:
          print(msg.author, msg.content, ctx.author)
          msgCount += 1
  if msgCount == 0:
    await ctx.send(f'No Results for {ctx.author.name}')
  else:
    await ctx.send(f'{ctx.author.name} {word} count: {msgCount}')

bot.run(my_secret)
