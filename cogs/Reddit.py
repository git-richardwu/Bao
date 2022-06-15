import discord
from discord.ext import commands
import random
import os
import praw

clientID = os.environ['clientID']
clientSecret = os.environ['clientSecret']
user_name = os.environ['username']
pass_word = os.environ['password']
userAgent = os.environ['userAgent']
secretSub = os.environ['secretSub']

reddit = praw.Reddit(client_id=clientID,
                     client_secret=clientSecret,
                     password=pass_word,
                     user_agent=userAgent,
                     username=user_name,
                     check_for_async=False)

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def r(ctx, sub='aww'):
        subreddit = reddit.subreddit(sub)
        hot_subs = []
    
        hot = subreddit.hot(limit=25)
        for submission in hot:
            hot_subs.append(submission)
    
        random_sub = random.choice(hot_subs)
    
        name = random_sub.title
        url = random_sub.url
    
        em = discord.Embed(title=name, description=url)
    
        em.set_image(url=url)
    
        await ctx.send(embed=em)


    @commands.command()
    async def t(ctx, sub='aww', time_filter="all"):
        subreddit = reddit.subreddit(sub)
        top_subs = []
    
        top = subreddit.top(time_filter)
        for submission in top:
            top_subs.append(submission)
    
        random_sub = random.choice(top_subs)
    
        name = random_sub.title
        url = random_sub.url
    
        em = discord.Embed(title=name, description=url)
    
        em.set_image(url=url)
    
        await ctx.send(embed=em)

def setup(client):
        client.add_cog(Reddit(client))