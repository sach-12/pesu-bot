import discord
from discord.ext import commands
from discord_slash import cog_ext, utils as sutils
# from discord.utils import get
import os
from dotenv import load_dotenv

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
        await sutils.manage_commands.remove_all_commands_in(bot_id=749484661717204992, bot_token=TOKEN, guild_id=742797665301168220)
        await sutils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=742797665301168220, cmd_name='pride', description="Flourishes you with the pride of PESU")

    #     self.admin = get(self.guildObj.roles, id=742800061280550923)
    #     self.bot_devs = get(self.guildObj.roles, id=750556082371559485)

    @cog_ext.cog_slash(name="nickchange", description="Change someone else's nickname")
    async def _nickchange(self, ctx, member:discord.Member, newname:str):
        # perms = discord.Permissions(manage_nicknames)
        perms = ctx.channel.permissions_for(ctx.author)
        if((perms.manage_nicknames) and (ctx.author.top_role.position > member.top_role.position)):
            try:
                await member.edit(nick=newname)
                await ctx.send(content=f"Nicely changed {member.name}'s name", hidden=True)
            except:
                await ctx.send(content="One cutie you are, trying to change sach's name only")
        else:
            await ctx.send(content="Soo cute you trying to change someone's nickname")

    @cog_ext.cog_slash(name="pride", description="Flourishes you with the pride of PESU")
    async def pride(self, ctx):
        await ctx.defer()
        await ctx.send(content="https://media.discordapp.net/attachments/742995787700502565/834782280236662827/Sequence_01_1.gif")



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