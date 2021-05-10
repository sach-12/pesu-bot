import discord
from discord.ext import commands
# from discord.utils import get
import os
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = 742797665301168220


class beta(commands.Cog):

    # slash = SlashCommand(commands.bot)
    def __init__(self, client):
        self.client = client
        # slash = SlashCommand(self.client, sync_commands = True)
        

    # This file will be used for obsolete code(if needed to be stored) or any other function
    # to be tested before moving to another cog

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)

    @commands.command(aliases=['restart'])
    async def _restart(self, ctx):
        BOT_TEST = 749473757843947671
        if ctx.author.id == 723377619420184668 or ctx.author.id == 718845827413442692:
            with open('cogs/verified.csv', 'r') as fp:
                await self.client.get_channel().send(file=discord.File(fp, 'verified.csv'))
            fp.close()
            p = subprocess.Popen(['python', 'start.py'])
            sys.exit(0)

    
    #     self.admin = get(self.guildObj.roles, id=742800061280550923)
    #     self.bot_devs = get(self.guildObj.roles, id=750556082371559485)


    # def run(*args):
    #     # return os.system('git commit')
    #     return os.system("git " + " ".join(list(args)))


    # def pull():
    #     run("pull", "origin", "master")


    # def commit():

    #     commit_message = "Bot Updating verified.csv"
    #     run("pull")
    #     run("commit", "-m", commit_message)
    #     run("push")


    # @commands.command(aliases=['u', 'update'])
    # async def _update(self, ctx):
    #     if((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
    #         pull()
    #         commit()
    #         await ctx.channel.send("You updated to git repo")
    #     else:
    #         await ctx.channel.send("You are not authorised to do that")


def setup(client):
    client.add_cog(beta(client))