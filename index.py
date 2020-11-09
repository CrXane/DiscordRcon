import discord
from discord.ext import commands
from rHLDS import Console

host = ''
port = 27015
password = ''

bot = commands.Bot(command_prefix='$') # example: $rcon status
token = ''

srv = Console(host=host, port=port, password=password)
srv.connect()

@bot.event
async def on_ready():
	print('Bot is running')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=host + ':' + str(port)))

@bot.command()
async def rcon(ctx, *args):
	await ctx.channel.send('```' + srv.execute(' '.join(args[:])) + '```')
		
bot.run(token)
