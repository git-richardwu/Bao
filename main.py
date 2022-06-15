import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

secret = os.environ['token']
client = commands.Bot(command_prefix='%')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('%c for command list'))


initial_extensions = []

for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
        initial_extensions.append("cogs." + cog[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

keep_alive()
client.run(secret)
