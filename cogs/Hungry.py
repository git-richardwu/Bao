import discord
from discord.ext import commands
import json
import os
import requests
import random
from replit import db

recipeAPI = os.environ['recipeAPI']

cuisines = ['american', 'cajun', 'chinese', 'french', 'indian', 'italian', 'jewish', 'korean', 'mediterranean', 'mexican', 'spanish', 'thai', 'vietnamese']

class Hungry(commands.Cog):
    def __init__(self, client):
        self.client = client

    def retrieveEvent(self, cuisine):
        if cuisine == "random":
          targetCuisine = random.choice(cuisines)
        elif cuisine in cuisines:
          targetCuisine = cuisine
        else:
          return #cuisine not supported :(
        responses = requests.get('https://api.spoonacular.com/recipes/complexSearch?cuisine='+ targetCuisine +'&addRecipeInformation=true&number=25&apiKey=' + recipeAPI)
        jsonData = json.loads(responses.text)
        ran = random.randint(0,24)
        randomDish = jsonData['results'][ran]
        return {"name": randomDish['title'], "link": randomDish['sourceUrl'], "image": randomDish['image']}

    @commands.command()
    async def hungry(self, ctx):
      userID = str(ctx.author.id)
      matches = db.prefix(userID)
      info = db[userID].value
      if len(matches) == 0:
        dish = self.retrieveEvent("random")
      else:
        subs = []
        for key, value in info.items():
          if value == True:
            subs.append(key)
        dish = self.retrieveEvent(random.choice(subs))
      name = dish["name"]
      source = dish["link"]
      image = dish["image"]
      em = discord.Embed(title=name, description=source)
      em.set_image(url=image)
      await ctx.send(embed=em)

    @commands.command()
    async def subscribe(self, ctx, topic):
      t = topic.lower()
      userID = str(ctx.author.id)
      matches = db.prefix(userID)
      if t in cuisines:
        if len(matches) == 0:
          post = {'american': False, 'chinese': False, 'french': False, 'indian': False, 'italian': False, 'jewish': False, 'korean': False, 'mediterranean': False, 'mexican': False, 'spanish': False, 'thai': False, 'vietnamese': False}
          await ctx.channel.send('New User Added!')
          db[userID] = post
        db[userID][t] = True
        await ctx.channel.send("Successfully subscribed to " + topic + " cuisine!")
      else:
        await ctx.channel.send("Cuisine Not Found. List of available cuisines: American, Cajun, Chinese, French, Indian, Italian, Jewish, Korean, Mediterranean, Mexican, Spanish, Thai, Vietnamese")
  
    @commands.command()
    async def unsubscribe(self, ctx, topic):
      t = topic.lower()
      userID = str(ctx.author.id)
      matches = db.prefix(userID)
      if t in cuisines:
        if len(matches) == 0:
          await ctx.channel.send("User not found :(")
        db[userID][t] = False
        await ctx.channel.send("Successfully unsubscribed to " + topic + " cuisine!")
      else:
        await ctx.channel.send("Cuisine Not Found. List of available cuisines: American, Cajun, Chinese, French, Indian, Italian, Jewish, Korean, Mediterranean, Mexican, Spanish, Thai, Vietnamese")

    @commands.command()
    async def subscriptions(self, ctx):
      userID = str(ctx.author.id)
      matches = db.prefix(userID)
      if len(matches) == 0:
          await ctx.channel.send("User not found :(")
          return
      values = db[userID]
      await ctx.channel.send(values.value)

    @commands.command()
    async def delete(self, ctx):
      del db[str(ctx.author.id)]
      await ctx.channel.send("Account deleted")

def setup(client):
        client.add_cog(Hungry(client))