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

    @mod_group.command(name='ban', description='Ban a user')
    @app_commands.describe(member='The user to be banned', reason='The reason for banning the user (optional)',
                           delete_msg_duration='Duration for which the messages of the user have to deleted in days')
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None,
                  delete_msg_duration: app_commands.Range[int, 0, 7] = 1):
        await interaction.response.defer(thinking=True)
        # Check if the user not an admin or mod
        if not interaction.user.guild_permissions.administrator and not interaction.user.guild_permissions.ban_members:
            await interaction.followup.send(content="Noob you can't do that", ephemeral=True)
            return
        # Check if the member is an admin or mod
        if member.guild_permissions.administrator or member.guild_permissions.ban_members:
            await interaction.followup.send(content="Gomma you can't ban admin/mod", ephemeral=True)
            return
        # Check if the member is the bot
        if member.bot:
            await interaction.followup.send(content="You dare ban one of my brothers you little twat!")
            return
        mem_name = member.name.replace('`', '').replace('*', '').replace('_', ' ')
        try:
            await member.ban(reason=reason, delete_message_days=delete_msg_duration)
        except Exception as e:
            await interaction.followup.send(f"Failed due to following error:\n`{e}`")
            return
        # Generate embed
        embed = discord.Embed(title=f"{mem_name} was banned!",
                              description=f"\n**Reason**: {reason if reason else 'Reason not specified.'}",
                              colour=0xff0000, timestamp=datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
        await interaction.followup.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(
        SlashMod(client), guild=discord.Object(id=os.getenv("GUILD_ID"))
    )
