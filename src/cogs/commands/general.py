import os
import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(alias=["ping", "latency"])
    async def ping(self, ctx: commands.Context):
        await ctx.typing()
        await ctx.reply(f"Pong!!!\nPing = `{round(self.client.latency * 1000, 2)}ms`")


async def setup(client: commands.Bot):
    await client.add_cog(
        General(client), guild=discord.Object(id=os.getenv("GUILD_ID"))
    )
