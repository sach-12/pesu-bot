import os
import discord
from discord import app_commands
from discord.ext import commands


class SlashMod(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    mod_group = app_commands.Group(name='mod', description='Moderation commands')

    def check_admin_mod(self, user: discord.Member):
        role_lst = [role.id for role in user.roles]
        return self.client.config["roles"]["admin"] in role_lst or self.client.config["roles"]["mod"] in role_lst

    @mod_group.command(name='kick', description='Kick a user')
    @app_commands.describe(member="The user to kick", reason="The reason for kicking the user (optional)")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer(thinking=True)
        # Check if the user is not an admin or mod
        if not self.check_admin_mod(interaction.user):
            await interaction.followup.send(content="Noob you can't do that", ephemeral=True)
            return
        # Check if the member is an admin or mod
        if self.check_admin_mod(member):
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
                              colour=0xff0000, timestamp=discord.utils.utcnow())
        embed.set_image(url="https://media.giphy.com/media/3o85xxDEtOKC7dzlXa/giphy.gif")
        await interaction.followup.send(embed=embed)
        # Writing to the logs thread
        embed.description = (f"{interaction.user.mention} kicked {member.mention}."
                             f"\n\n**Reason**: {reason if reason else 'Reason not specified.'}")
        embed.set_footer(text=f"Kicked by {interaction.user.name}").set_image(url=None)
        await self.client.get_guild(self.client.config['guild_id']).get_channel_or_thread(
            self.client.config['threads']['kick_logs']).send(embed=embed)

    @mod_group.command(name='ban', description='Ban a user')
    @app_commands.describe(member='The user to be banned', reason='The reason for banning the user (optional)',
                           delete_msg_duration='Duration for which the messages of the user have to deleted in days')
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None,
                  delete_msg_duration: app_commands.Range[int, 0, 7] = 1):
        await interaction.response.defer(thinking=True)
        # Check if the user not an admin or mod
        if not self.check_admin_mod(interaction.user):
            await interaction.followup.send(content="Noob you can't do that", ephemeral=True)
            return
        # Check if the member is an admin or mod
        if self.check_admin_mod(member):
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
                              colour=0xff0000, timestamp=discord.utils.utcnow())
        embed.set_image(url="https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif")
        await interaction.followup.send(embed=embed)
        # Writing to the logs thread
        embed.description = (f"{interaction.user.mention} banned {member.mention}."
                             f"\n\n**Reason**: {reason if reason else 'Reason not specified.'}")
        embed.set_footer(text=f"Banned by {interaction.user.name}").set_image(url=None)
        await self.client.get_guild(self.client.config['guild_id']).get_channel_or_thread(
            self.client.config['threads']['ban_logs']).send(embed=embed)

    @mod_group.command(name='untimeout', description='To remove a timeout a user')
    @app_commands.describe(member="The user whose timeout is to be removed.")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(thinking=True)
        # Check if the user not an admin or mod
        if not self.check_admin_mod(interaction.user):
            await interaction.followup.send(content="Noob you can't do that", ephemeral=True)
            return
        try:
            await member.timeout(None)
        except Exception as e:
            await interaction.followup.send(f"Failed due to following error:\n`{e}`")
            return
        await interaction.followup.send(f"Successfully removed timeout for {member.mention}")


async def setup(client: commands.Bot):
    await client.add_cog(SlashMod(client), guild=discord.Object(id=client.config['guild_id']))
