import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_slash import SlashCommand

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!', help_command=None, intents=discord.Intents().all())
slash = SlashCommand(client, sync_commands = True, sync_on_cog_reload = True)
BOT_LOGS = 786084620944146504

@client.command(aliases = ['loadit'])
async def load(ctx, extension):
    bot_devs = discord.utils.get(ctx.guild.roles, id=750556082371559485)
    if(bot_devs in ctx.author.roles):
        try:
            client.load_extension(f"cogs.{extension}")
            success = f"cogs.{extension} was loaded succesfully"
            await ctx.channel.send(success)
            await client.get_channel(BOT_LOGS).send(success)
        except Exception as e:
            await ctx.channel.send(e)
    else:
        await ctx.channel.send("Unauthorised")


@client.command(aliases = ['unloadit'])
async def unload(ctx, extension):
    bot_devs = discord.utils.get(ctx.guild.roles, id=750556082371559485)
    if(bot_devs in ctx.author.roles):
        try:
            client.unload_extension(f"cogs.{extension}")
            success = f"cogs.{extension} was unloaded succesfully"
            await ctx.channel.send(success)
            await client.get_channel(BOT_LOGS).send(success)
        except Exception as e:
            await ctx.channel.send(e)
    else:
        await ctx.channel.send("Unauthorised")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)
