import os
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


async def setup(client: commands.Bot):
    await client.add_cog(Events(client), guild=discord.Object(id=os.getenv("GUILD_ID")))
