# WordRanking Discord Bot
# This bot will take a search query from a user and output the user who has used that word the most and how many times.
# There will be leaderboards of the top people who used the word.

import discord
from discord.ext import commands
import os
import sqlite3

my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='!')

# Allows user to view the message leaderboards for a specific keyword.
# Connect to database
with sqlite3.connect('ChatLogs.db') as db:
    c = db.cursor()

#DEV ONLY, UPLOADS ALL CHATLOGS TO DB
@bot.command()
async def uploadranks(ctx):
    embedVar = discord.Embed(title=f'Gathering Data...', color=0x00ff00)
    embed_msg = await ctx.send(embed=embedVar)

    channel = discord.utils.get(ctx.guild.channels, name="general")
    messages = await ctx.channel.history(limit=None).flatten()

    upload_embed = discord.Embed(title=f'Uploading Chat Logs... ({len(messages)})', color=0x00ff00)

    await embed_msg.edit(embed=upload_embed)

    for msg in messages:
        if not msg.content.startswith("!"):
            c.execute('INSERT INTO ChatLogDeets(guild_id, user_id, msg_content, msg_created_at) VALUES(?,?,?,?)', (msg.guild.id, msg.author.id, msg.content, msg.created_at))
            db.commit()


    success_embed = discord.Embed(title=f"Successfully Uploaded Chat Logs: {len(messages)} Messages", color=0x00ff00)
    await embed_msg.edit(embed=success_embed)



#Display how often a word was used.
@bot.command()
async def wordrank(ctx, *, word: str):
    msgCount = 0

    embedVar = discord.Embed(title=f'Calculating Total Message Count for Keyword: {word}', color=0x00ff00)
    embed_msg = await ctx.send(embed=embedVar)

    channel = discord.utils.get(ctx.guild.channels, name="general")
    messages = await ctx.channel.history(limit=None).flatten()

    for msg in messages:
      if str(msg.author) != "WordRankings#3933":
        msg.content = msg.content.lower()
        if word in msg.content:
          if '!keyword' not in msg.content and '!wordrank' not in msg.content:
              msgCount += 1
    
    success_embed = discord.Embed(title=f"Total '{word}' count: {msgCount}", color=0x00ff00)
    fail_embed = discord.Embed(title=f'No Results for {word}', color=0xff0000)

    if msgCount == 0:
      await embed_msg.edit(embed=fail_embed)
    else:
      await embed_msg.edit(embed=success_embed)
    

# SUPREMELY SLOW/CRASHES IF USED ON LARGE SERVER.
@bot.command()
async def keyword(ctx, *, word: str):
    msgCount = 0

    embedVar = discord.Embed(title=f"Calculating {ctx.author.name}'s Message Count for Keyword: {word}", color=0x00ff00)
    embed_msg = await ctx.send(embed=embedVar)

    channel = discord.utils.get(ctx.guild.channels, name="general")
    messages = await ctx.channel.history(limit=None).flatten()

    for msg in messages:
      if str(msg.author) != "WordRankings#3933":
        msg.content = msg.content.lower()
        if word in msg.content:
          if '!keyword' not in msg.content:
              msgCount += 1

    success_embed = discord.Embed(title=f'{ctx.author.name} {word} count: {msgCount}', color=0x00ff00)
    fail_embed = discord.Embed(title=f'No Results for {ctx.author.name}', color=0xff0000)

    if msgCount == 0:
      await embed_msg.edit(embed=fail_embed)
    else:
      await embed_msg.edit(embed=success_embed)

bot.run(my_secret)
