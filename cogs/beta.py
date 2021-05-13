import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = 742797665301168220



class beta(commands.Cog):

    # slash = SlashCommand(commands.bot)
    def __init__(self, client):
        self.client = client        

    # This file will be used for obsolete code(if needed to be stored) or any other function
    # to be tested before moving to another cog

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)

    #     self.admin = get(self.guildObj.roles, id=742800061280550923)
    #     self.bot_devs = get(self.guildObj.roles, id=750556082371559485)



def setup(client):
    client.add_cog(beta(client))
