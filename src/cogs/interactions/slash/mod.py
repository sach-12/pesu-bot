import os
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands


class SlashMod(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    mod_group = app_commands.Group(name='mod', description='Moderation commands')

    @mod_group.command(name='kick', description='Kick a user')
    @app_commands.describe(member="The user to kick", reason="The reason for kicking the user (optional)")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer(thinking=True)
        # Check if the user is not an admin or mod
        if not interaction.user.guild_permissions.administrator and not interaction.user.guild_permissions.kick_members:
            await interaction.followup.send(content="Noob you can't do that", ephemeral=True)
            return
        # Check if the member is an admin or mod
        if member.guild_permissions.administrator or member.guild_permissions.kick_members:
            await interaction.followup.send(content="Gomma you can't kick admin/mod", ephemeral=True)
            return
        # Check if the member is the bot
        if member.bot:
            await interaction.followup.send(content="You dare kick one of my brothers you little twat!", ephemeral=True)
            return
        mem_name = member.name.replace('`', '').replace('*', '').replace('_', ' ')
        try:
            await member.kick(reason=reason)
        except Exception as e:
            await interaction.followup.send(f"Failed due to following error:\n`{e}`")
            return
        # Generate embed
        embed = discord.Embed(title=f"{mem_name} was kicked!",
                              description=f"\n**Reason**: {reason if reason else 'Reason not specified.'}",
                              colour=0xff0000, timestamp=datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/3o85xxDEtOKC7dzlXa/giphy.gif")
        await interaction.followup.send(embed=embed)

    @commands.command(name='reload', help='To reload all cogs.')
    async def reload(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Noob you can't do that")
            return
        # Reload cogs
        for root, dirs, files in os.walk("cogs"):
            for f in files:
                if f.endswith(".py"):
                    cog = f"{root}.{f[:-3]}"
                    cog = cog.replace("\\", ".")
                    await self.client.reload_extension(cog)
                    self.client.logger.info(f"Reloaded {cog}")
        await ctx.send('Reloaded!')


async def setup(client: commands.Bot):
    await client.add_cog(
        SlashMod(client), guild=discord.Object(id=os.getenv("GUILD_ID"))
    )
