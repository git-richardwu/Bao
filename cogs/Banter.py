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

shower_quotes = [
    "Guess we're not doing anything today.", "See you in 3 hours.",
    "You can just say you don't want to hang out with us.",
    "Convenient timing as always.", "gOnNa Go SHoWEr.",
    "Out of curiosity, what does your water bill look like? "
]

talking = ["bao", "how are you", "what's on your mind", "what is on your mind"]

names = ["omg bb", "omg bby", "boo boo", "bb"]

name_responses = [
    "💤", "Get a room already.", "Can a bot get some peace and quiet here?",
    "TRYING TO SLEEP HERE.", "Can ya'll keep it down?"
]

gn_responses = [
  "Imagine sleeping.", "Could not be me.", "gn", "night", "About time."
]

yesNo = ['✅', '❎']

counter = 0

reddit = praw.Reddit(client_id=clientID,
                     client_secret=clientSecret,
                     password=pass_word,
                     user_agent=userAgent,
                     username=user_name,
                     check_for_async=False)

class Banter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def c(self, ctx):
        await ctx.channel.send(
            '**%c** = list of commands\n**%e** = example commands\n**%r {subreddit}** = random Hot post from {subreddit}. (default: r/aww)\n**%t {subreddit} {time_filter}** = random top 10 post from {subreddit} from {time_filter}. (default: all)\n**%subscribe {cuisine}** = create a user profile and subscribe to specific cuisine.\n**%unsubscribe {cuisine}** = unsubscribe to specific cuisine.\n**%subscriptions** = view active subscriptions\n**%hungry** = get a recipe from subscription. (random if user does not have a profile)\n**%delete** = delete user profile. Do not try to talk to me.'
        )

    @commands.command()
    async def e(self, ctx):
        await ctx.channel.send(
            '%r Eyebleach = random Hot post from r/Eyebleach.\n%r CatsISUOTTATFO = random Top posts of all time from r/CatsISUOTTATFO.\n%t DisneyEyes month = random Top posts of this month from r/DisneyEyes.\n%t birdswitharms day = random Top posts of the day from r/birdswitharms.\n%subscribe chinese = subscribe to chinese cuisine. (if profile not found, creates new user profile)\n%unsubscribe chinese = unsubscribe to chinese cuisine\n%subscriptions = show user subscriptions\n%hungry = fetch recipe\n%delete = delete user subscriptions and profile from database'
        )

    def get_pasta(self):
      subreddit = reddit.subreddit(secretSub)
      all_pasta = []
      # top = subreddit.hot(limit=50)
      top = subreddit.top('week')
      for submission in top:
          if len(submission.selftext) < 2000:
              all_pasta.append(submission)
  
      random_pasta = random.choice(all_pasta)
      alfredo = random_pasta.selftext
      return (alfredo)

    @commands.command()
    async def quit(self, ctx):
        await ctx.send("Shutting down the bot")
        return await self.client.logout()
  
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        msg = message.content.lower()

        if any(phrase in msg for phrase in talking):
            res = await message.channel.send(self.get_pasta())
            for emoji in yesNo:
                await res.add_reaction(emoji)

        elif any(name in msg for name in names):
            global counter
            counter += 1
            if (counter % 2) == 0:
                await message.channel.send(random.choice(name_responses))

        elif msg.startswith('hola'):
            await message.channel.send("adiós 👋")

        elif "love you" in msg:
            await message.add_reaction('👀')

        elif "shower" in msg:
            await message.channel.send(random.choice(shower_quotes))

        elif "good night" in msg:
            await message.channel.send(random.choice(gn_responses))

def setup(client):
        client.add_cog(Banter(client))