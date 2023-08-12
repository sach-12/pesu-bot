import os
import discord
from discord import app_commands
from discord.ext import commands


class SlashGeneral(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Get the bot's latency")
    async def ping_slash(self, ctx: discord.Interaction):
        await ctx.response.defer()
        await ctx.followup.send(
            content=f"Pong!!!\nPing = `{round(self.client.latency * 1000)}ms`"
        )


async def setup(client: commands.Bot):
    await client.add_cog(
        SlashGeneral(client), guild=discord.Object(id=os.getenv("GUILD_ID"))
    )
