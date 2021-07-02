import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from discord_slash import cog_ext, utils
import os
import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np
from discord_slash.utils.manage_commands import create_option
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')


GUILD_ID = 742797665301168220
MOD_LOGS = 778678059879890944
TOKEN = os.getenv('DISCORD_TOKEN')


class misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.purge = '`!p` or `!purge`\n!p {amount}\n\nPurges the specified number of messages(limit=1000)'
        self.echo = '`!e` or `!echo`\n!e {Channel mention} {Text}\n\nEchoes a message through the bot to the specified channel'
        self.mute = '`!mute`\n!mute {Member mention} {Time} {Reason: optional}\n\nMutes the user for the specified time\nLimit: 14 days'
        self.unmute = '`!unmute`\n!unmute {Member mention}\n\nUnmutes the user'
        self.lock = '`!lock`\n!lock {Channel mention} {Reason: optional}\n\nLocks the specified channel'
        self.unlock = '`!unlock`\n!unlock {Channel mention}\n\nUnlocks the specified channel'
        self.kick = '`!kick`\n!kick {Member mention} {Reason: optional}\n\nKicks the member from the server'
        self.confessions = {}

    @commands.Cog.listener()
    async def on_ready(self):
        flush_confessions.start()
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=742800061280550923)
        self.mods = get(self.guildObj.roles, id=742798158966292640)
        self.bot_devs = get(self.guildObj.roles, id=750556082371559485)
        self.bots = get(self.guildObj.roles, id=746226955094851657)
        self.pesu_bot = get(self.guildObj.roles, id=801011477851013150)
        self.muted = get(self.guildObj.roles, id=775981947079491614)

    @commands.Cog.listener()
    async def on_message(self, message):
        if('chad' in message.content.lower().replace('‎', '').replace('chadwick', '')):
            if((self.admin in message.author.roles) or (self.mods in message.author.roles) or (self.bots in message.author.roles)):
                pass
            else:
                await message.channel.send(f"no telling chad {message.author.mention} <:tengue_fold:762662965387460629>")
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if('chad' in after.content.lower().replace('‎', '').replace('chadwick', '')):
            if((self.admin in after.author.roles) or (self.mods in after.author.roles) or (self.bots in after.author.roles)):
                pass
            else:
                await after.channel.send("nin amn you think you are smart huh")
                await after.channel.send(f"no editing to chad either {after.author.mention} <:tengue_fold:762662965387460629>")
        pass

    @commands.command(aliases=['c', 'count'])
    async def _count(self, ctx, *roleName):
        roleName = ' '.join(roleName)
        # convert it back into string and split it at '&' and strip the individual roles.
        try:
            roleName = roleName.split('&')
        except:
            pass
        temp = []
        for i in roleName:
            temp.append(i.strip())
        roleName = temp
        await ctx.channel.send(f"Got request for role {str(roleName)}")
        if(roleName == ['']):
            for guild in self.client.guilds:
                await ctx.channel.send(f"We have {len(guild.members)} people here, wow!!")
        else:
            thisRole = []
            for roles in roleName:
                thisRole.append(get(ctx.guild.roles, name=roles))
            for guild in self.client.guilds:
                count = 0
                for member in guild.members:
                    boolean = True
                    # bool will be true only if all the roles passed as args are present
                    for roles in thisRole:
                        if roles not in member.roles:
                            boolean = False
                    if boolean:
                        count += 1
            await ctx.channel.send(f"{str(count)} people has role {str(thisRole)}")

    @commands.command(aliases=['p', 'purge'])
    async def _clear(self, ctx, amt=0):
        purge_embed = discord.Embed(
            title="Purge", color=0x48BF91, desciption=self.purge)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            if(amt == 0):
                await ctx.channel.send("Lawda tell how much you want to purge", embed=purge_embed)
                return
            if(amt > 1000):
                await ctx.channel.send("Lawda, limit is 1000 okay?", embed=purge_embed)
                return
            await ctx.channel.purge(limit=amt)
        else:
            await ctx.channel.send(f"{ctx.author.mention} You are not authorised to do that")

    @commands.command(aliases=['e', 'echo'])
    async def _echo(self, ctx, dest: discord.TextChannel = None, *, message: str = ''):
        echo_embed = discord.Embed(
            title="Echo", color=0x48BF91, desciption=self.echo)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            if(dest == None):
                await ctx.channel.send(embed=echo_embed)
                return
            attachment = ctx.message.attachments
            if(dest.id == ctx.channel.id):
                await ctx.channel.purge(limit=1)
            if(message != ''):
                await dest.send(message)
            if(len(attachment) != 0):
                await attachment[0].save(attachment[0].filename)
                await dest.send(file=discord.File(attachment[0].filename))
                os.remove(attachment[0].filename)
        else:
            await ctx.channel.send("Sucka you can't do that")

    @ commands.command(aliases=['mute'])
    async def _mute(self, ctx, member: discord.Member = None, time='', *, reason: str = 'no reason given'):
        mute_help_embed = discord.Embed(
            title="Mute", color=0x48BF91, description=self.mute)

        # if(ctx.author.mention == member.mention):
        #     mod = self.client.get_user(749484661717204992)
        # else:
        #     mod = ctx.author

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if(member != None):
                seconds = 0
                if(time.lower().endswith("d")):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                if(time.lower().endswith("h")):
                    seconds += int(time[:-1]) * 60 * 60
                elif(time.lower().endswith("m")):
                    seconds += int(time[:-1]) * 60
                elif(time.lower().endswith("s")):
                    seconds += int(time[:-1])

                if((seconds <= 0) or (seconds > 1209600)):
                    await ctx.channel.send(f"{ctx.author.mention}, please enter a valid amount of time", embed=mute_help_embed)
                else:
                    if(self.muted in member.roles):
                        await ctx.channel.send("Lawda he's already muted means how much more you'll do")
                    else:
                        if((self.admin in member.roles) or (self.mods in member.roles)):
                            await ctx.channel.send("Lawda, he's an admin/mod. I can't mute him")
                        elif(self.bots in member.roles):
                            await ctx.channel.send("You dare try to mute my own kind")
                        else:
                            await member.add_roles(self.muted)
                            mute_embed = discord.Embed(
                                title="Mute", color=0xff0000)
                            mute_user = f"{member.mention} was muted"
                            mute_embed.add_field(
                                name="Muted user", value=mute_user)
                            await ctx.channel.send(embed=mute_embed)
                            mute_embed_logs = discord.Embed(
                                title="Mute", color=0xff0000)
                            mute_details_logs = f"{member.mention}\t Time: {time}\n Reason: {reason}\n Moderator: {ctx.author.mention}"
                            mute_embed_logs.add_field(
                                name="Muted user", value=mute_details_logs)
                            await self.client.get_channel(MOD_LOGS).send(embed=mute_embed_logs)
                            await asyncio.sleep(seconds)
                            if(self.muted in member.roles):
                                unmute_embed = discord.Embed(
                                    title="Unmute", color=0x00ff00)
                                unmute_user = f"{member.mention} welcome back"
                                unmute_embed.add_field(
                                    name="Unmuted user", value=unmute_user)
                                await ctx.channel.send(embed=unmute_embed)
                                unmute_embed_logs = discord.Embed(
                                    title="Unmute", color=0x00ff00)
                                unmute_details_logs = f"{member.mention}\n Moderator: Auto"
                                unmute_embed_logs.add_field(
                                    name="Unmuted user", value=unmute_details_logs)
                                await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                                await member.remove_roles(self.muted)
            else:
                await ctx.channel.send(f"{ctx.author.mention}, mention the user, not just the name", embed=mute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")

    @ commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, member: discord.Member):
        unmute_help_embed = discord.Embed(
            title="Unmute", color=0x48BF91, description=self.unmute)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            try:
                if(self.muted not in member.roles):
                    await ctx.channel.send("Lawda he's not muted only means")
                else:
                    unmute_embed = discord.Embed(
                        title="Unmute", color=0x00ff00)
                    unmute_user = f"{member.mention} welcome back"
                    unmute_embed.add_field(
                        name="Unmuted user", value=unmute_user)
                    await ctx.channel.send(embed=unmute_embed)
                    unmute_embed_logs = discord.Embed(
                        title="Unmute", color=0x00ff00)
                    unmute_details_logs = f"{member.mention}\n Moderator: {ctx.author.mention}"
                    unmute_embed_logs.add_field(
                        name="Unmuted user", value=unmute_details_logs)
                    await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                    await member.remove_roles(self.muted)
            except:
                await ctx.channel.send(embed=unmute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")

    @ commands.command(aliases=['lock'])
    async def _lock_channel(self, ctx, channel, *, reason: str = 'no reason given'):
        lock_help_embed = discord.Embed(
            title="Embed", color=0x48BF91, description=self.lock)

        overwrites = discord.PermissionOverwrite(
            send_messages=False, view_channel=False)
        channel = str(channel)
        newChannel = ''
        for i in channel:
            if i in "0123456789":
                newChannel += i
        newChannel = int(newChannel)
        try:
            channelObj = self.client.get_channel(newChannel)
        except:
            await ctx.channel.send(embed=lock_help_embed)
            return

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await channelObj.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            lock_embed = discord.Embed(
                title="Channel Locked :lock:", color=0xff0000, description=reason)
            await channelObj.send(embed=lock_embed)
            lock_message = discord.Embed(
                title="", color=0x00ff00, description=f"Locked {channelObj.mention}")
            await ctx.channel.send(embed=lock_message)
            lock_logs = discord.Embed(title="Lock", color=0xff0000)
            lock_logs.add_field(name="Channel", value=channelObj.mention)
            lock_logs.add_field(name="Moderator", value=ctx.author.mention)
            await self.client.get_channel(MOD_LOGS).send(embed=lock_logs)
        else:
            await ctx.channel.send("Lawda, I am not dyno to let you do this")

    @ commands.command(aliases=['unlock'])
    async def _unlock_channel(self, ctx, channel):
        unlock_help_embed = discord.Embed(
            title="Unlock", color=0x48BF91, description=self.unlock)
        overwrites = discord.PermissionOverwrite(view_channel=False)

        channel = str(channel)
        newChannel = ''
        for i in channel:
            if(i in "0123456789"):
                newChannel += i
        newChannel = int(newChannel)

        try:
            channelObj = self.client.get_channel(newChannel)
        except:
            await ctx.channel.send(embed=unlock_help_embed)
            return
        perms = channelObj.overwrites_for(ctx.guild.default_role)

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if ((perms.view_channel == False) and (perms.send_messages == False)):
                await channelObj.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                unlock_embed = discord.Embed(
                    title="Channel Unlocked :unlock:", color=0x00ff00)
                await channelObj.send(embed=unlock_embed)
                unlock_message = discord.Embed(
                    title="", color=0x00ff00, description=f"Unlocked {channelObj.mention}")
                await ctx.channel.send(embed=unlock_message)
                unlock_logs = discord.Embed(title="Unlock", color=0x00ff00)
                unlock_logs.add_field(name="Channel", value=channelObj.mention)
                unlock_logs.add_field(
                    name="Moderator", value=ctx.author.mention)
                await self.client.get_channel(MOD_LOGS).send(embed=unlock_logs)
            else:
                await ctx.send("Lawda that channel is already unlocked")
        else:
            await ctx.channel.send("Lawda, I am not dyno to let you do this")

    @ commands.command(aliases=['contribute', 'support'])
    async def _support(self, ctx, *params):
        Embeds = discord.Embed(title="Contributions", color=0x00ff00)
        Embeds.add_field(
            name="Github repo", value="https://github.com/sach-12/pesu-bot", inline=False)
        Embeds.add_field(
            name='\u200b', value="If you wish to contribute to the bot, run these steps:", inline=False)
        rules = {
            0: "Pull the latest main branch, dont start working with any deprecated versions",

            1: "Create a new branch called `beta-(discord-username)`",

            2: "Do whatever changes you wish to do and create a pull request with the following information furnished in the request message: 'The cog you wish to change | What did you change'",

            3: "Wait for approval for reviewers. Your PR may be directly accepted or requested for further changes.",

        }
        for ruleNo in rules:
            Embeds.add_field(name='\u200b', value="`" +
                             str(ruleNo) + '`: ' + rules[ruleNo], inline=False)

        stark = ctx.guild.get_member(718845827413442692).mention
        flabby = ctx.guild.get_member(467341580051939339).mention
        e11i0t = ctx.guild.get_member(621283810926919680).mention
        sach = ctx.guild.get_member(723377619420184668).mention
        Embeds.add_field(name="Reviewers", value="`ArvindAROO` - {}\n `Flab-E` - {}\n `Mre11i0t` - {} and\n `sach-12` - {}".format(
            stark, flabby, e11i0t, sach), inline=False)
        Embeds.add_field(
            name="Important", value="**Under no circumstances is anyone allowed to merge to the main branch.**", inline=False)
        await ctx.send(embed=Embeds)

    @commands.command(aliases=['poll'])
    async def poll_command(self, ctx, *, msg: str = ''):
        poll_help = discord.Embed(title="Start a poll", color=0x2a8a96)
        poll_help.add_field(
            name="!poll", value="Usage:\n!poll Message [Option1][Option2]...[Option9]", inline=False)
        poll_help.add_field(
            name="\u200b", value="To get results of a poll, use `!pollshow [message ID]`", inline=False)
        if(msg == ''):
            await ctx.channel.send(embed=poll_help)
            return
        msg_1 = msg.split('[')
        poll_list = []
        for i in msg_1:
            j = (i.replace(']', '').replace('[', ''))
            if(j == ''):
                continue
            poll_list.append(j.strip())
        if(len(poll_list) == 1):
            await ctx.channel.send("Not enough parameters")
            await ctx.channel.send(embed=poll_help)
        elif(len(poll_list) == 2):
            await ctx.channel.send("You need more than one choice")
        elif(len(poll_list) > 10):
            await ctx.channel.send("Can't have more than nine choice")
        else:
            question = poll_list[0]
            options = poll_list[1:]
            reactions_list = [':one:', ':two:', ':three:', ':four:',
                              ':five:', ':six:', ':seven:', ':eight:', ':nine:']
            new_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣',
                        '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            poll_embed = discord.Embed(title=question, color=0x7289da, timestamp=datetime.now(IST))
            for i in range(len(poll_list)-1):
                poll_embed.add_field(
                    name="\u200b", value=f"{reactions_list[i]} {options[i]}", inline=False)
            poll_embed.set_footer(text=f"Poll by {ctx.author}")
            await ctx.channel.send(embed=poll_embed)
            required_message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
            for i in range(len(poll_list)-1):
                await required_message.add_reaction(new_list[i])

    @commands.command(aliases=['pollshow', 'ps'])
    async def poll_results(self, ctx, msgid: int):
        try:
            msgObj = await ctx.channel.fetch_message(msgid)
        except:
            await ctx.channel.send("Poll not found. Make sure you're on the same channel as the poll and try again")
            return
        results = []
        choices = []
        poll_embed = msgObj.embeds[0]
        for i in msgObj.reactions:
            results.append(i.count - 1)
        for i in poll_embed.fields:
            choices.append(i.value.split(':')[2].strip())
        y = np.array(results)
        plt.pie(y, labels=choices)
        plt.legend(loc=2)
        plt.savefig('ps.jpg')
        file1 = discord.File('ps.jpg')
        os.remove('ps.jpg')
        poll_results = discord.Embed(title="Poll Results", color=0x7289da)
        for j in range(len(choices)):
            poll_results.add_field(
                name=choices[j], value=f"{results[j]} votes", inline=False)
        poll_results.set_image(url="attachment://ps.jpg")
        await ctx.channel.send(embed=poll_results, file=file1)
        plt.close()

    @ commands.command(aliases=['kick'])
    async def _kick(self, ctx, member, *reason):
        kick_help_embed = discord.Embed(
            title="Kick", color=0x48BF91, desciption=self.kick)

        reason = list(reason)
        reason = ' '.join(reason)
        if(reason == ""):
            reason = "no reason given"
        if '@' in str(member):
            member = str(member)
            id = ''
            for i in member:
                if i in '1234567890':
                    id += i
            member = int(id)
            try:
                member = ctx.message.guild.get_member(member)
            except:
                await ctx.channel.send(embed=kick_help_embed)
                return
        else:
            await ctx.send("Mention the user and not just the name", embed=kick_help_embed)
            return

        # a small little spartan easter egg
        if ((self.bots in member.roles) and (ctx.author.id == 621677829100404746)):
            await ctx.send("AAAAAAAAAAAAAHHHHHHHHHHHH no no no not again spartan!!! NOOOO")
            return

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if(self.bots in member.roles):
                await ctx.channel.send("You dare to kick one of my brothers huh")
            elif((self.admin in member.roles) or (self.mods in member.roles)):
                await ctx.channel.send("Gomma you can't kick admin/mod")
            else:
                await ctx.guild.kick(member)
                kick_embed = discord.Embed(
                    title="", color=0xff0000, description=f"{member.mention}** was kicked**")
                await ctx.channel.send(embed=kick_embed)
                kick_logs = discord.Embed(title="Kick", color=0xff0000)
                kick_logs.add_field(name="Moderator", value=ctx.author.mention)
                kick_logs.add_field(name="Reason", value=reason)
                await self.client.get_channel(MOD_LOGS).send(embed=kick_logs)
                try:
                    await member.send(f"You were kicked from the PESU 2019 Batch server\n Reason: {reason}")
                except:
                    await ctx.send("that lawda fellow hasn't opened his dms only")
        else:
            await ctx.channel.send("Lawda, I am not dyno to let you do this")

    @commands.command(aliases=['pull'])
    async def git_pull(self, ctx):
        if ctx.author.id == 723377619420184668 or ctx.author.id == 718845827413442692:
            sys.stdout.flush()
            p = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
            for line in iter(p.stdout.readline, ''):
                if not line:
                    break
                await ctx.channel.send(str(line.rstrip(), 'utf-8', 'ignore'))
            sys.stdout.flush()
        else:
            await ctx.channel.send("Lawda you can't execute this command")

    @commands.command(aliases=['restart'])
    async def _restart(self, ctx):
        BOT_TEST = 749473757843947671
        if ctx.author.id == 723377619420184668 or ctx.author.id == 718845827413442692:
            await self.git_pull(ctx)
            with open('cogs/verified.csv', 'r') as fp:
                await self.client.get_channel(BOT_TEST).send(file=discord.File(fp, 'verified.csv'))
            fp.close()
            p = subprocess.Popen(['python3', 'start.py'])
            sys.exit(0)
        else:
            await ctx.channel.send("Cuteeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            await asyncio.sleep(1)
            await ctx.channel.send("NO")

    @commands.command(aliases=['enableconfess'])
    async def flush_slash(self, ctx):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            await ctx.channel.trigger_typing()
            await utils.manage_commands.remove_all_commands(bot_id=749484661717204992, bot_token=TOKEN, guild_ids=None)
            await utils.manage_commands.remove_all_commands(bot_id=749484661717204992, bot_token=TOKEN, guild_ids=[GUILD_ID])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='pride', description='Flourishes you with the pride of PESU', options=[create_option(name="msg_id", description="Message ID of any message you wanna reply to with the pride", option_type=3, required=False)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='nickchange', description='Change someone else\'s nickname', options=[create_option(name="member", description="The member whose nickname you desire to change", option_type=6, required=True), create_option(name="new_name", description="The new name you want to give this fellow", option_type=3, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confess', description='Submits an anonymous confession', options=[create_option(name="confession", description="Opinion or confession you want to post anonymously", option_type=3, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessban', description='Bans a user from submitting confessions who submitted a confession based on message ID', options=[create_option(name="msg_id", description="Message ID of the confession", option_type=3, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessbanuser', description="Bans a user from submitting confessions", options=[create_option(name="member", description="User/Member to ban", option_type=6, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessunbanuser', description="Unbans a user from submitting confessions", options=[create_option(name="member", description="User/Member to unban", option_type=6, required=True)])
            await ctx.channel.send("Done")
            enabled = discord.Embed(title="Announcement from the mods", color=discord.Color.green(
            ), description="The confessions features has been enabled")
            await self.client.get_channel(860224115633160203).send(embed=enabled)
            overwrites = discord.PermissionOverwrite(view_channel=False)
            await self.client.get_channel(860224115633160203).set_permissions(ctx.guild.default_role, overwrite=overwrites)
        else:
            await ctx.channel.send("You are not authorised for this")

    @commands.command(aliases=['disableconfess'])
    async def disable_confess(self, ctx):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await ctx.channel.trigger_typing()
            await utils.manage_commands.remove_all_commands(bot_id=749484661717204992, bot_token=TOKEN, guild_ids=None)
            await utils.manage_commands.remove_all_commands(bot_id=749484661717204992, bot_token=TOKEN, guild_ids=[GUILD_ID])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='pride', description='Flourishes you with the pride of PESU', options=[create_option(name="msg_id", description="Message ID of any message you wanna reply to with the pride", option_type=3, required=False)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='nickchange', description='Change someone else\'s nickname', options=[create_option(name="member", description="The member whose nickname you desire to change", option_type=6, required=True), create_option(name="new_name", description="The new name you want to give this fellow", option_type=3, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessban', description='Bans a user from submitting confessions who submitted a confession based on message ID', options=[create_option(name="msg_id", description="Message ID of the confession", option_type=3, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessbanuser', description="Bans a user from submitting confessions", options=[create_option(name="member", description="User/Member to ban", option_type=6, required=True)])
            await utils.manage_commands.add_slash_command(bot_id=749484661717204992, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confessunbanuser', description="Unbans a user from submitting confessions", options=[create_option(name="member", description="User/Member to unban", option_type=6, required=True)])
            await ctx.channel.send("Done")
            disabled = discord.Embed(title="Announcement from the mods", color=discord.Color.red(
            ), description="The confessions features has been disabled")
            await self.client.get_channel(860224115633160203).send(embed=disabled)
            overwrites = discord.PermissionOverwrite(
                send_messages=False, view_channel=False)
            await self.client.get_channel(860224115633160203).set_permissions(ctx.guild.default_role, overwrite=overwrites)
        else:
            await ctx.channel.send("You are not authorised for this")

    @ cog_ext.cog_slash(name="nickchange", description="Change someone else's nickname", options=[create_option(name="member", description="The member whose nickname you desire to change", option_type=6, required=True), create_option(name="new_name", description="The new name you want to give this fellow", option_type=3, required=True)])
    async def nickchange(self, ctx, member: discord.Member, new_name: str):
        perms = ctx.channel.permissions_for(ctx.author)
        if((perms.manage_nicknames) and (ctx.author.top_role.position > member.top_role.position)):
            try:
                await member.edit(nick=new_name)
                await ctx.send(content=f"Nicely changed {member.name}'s name", hidden=True)
            except:
                await ctx.send(content="Can't do this one man!")
        else:
            await ctx.send(content=f"Soo cute you trying to change {member.name}'s nickname")

    @ cog_ext.cog_slash(name="pride", description="Flourishes you with the pride of PESU", options=[create_option(name="msg_id", description="Message ID of any message you wanna reply to with the pride", option_type=3, required=False)])
    async def pride(self, ctx, *, msg_id: str = ''):
        # await ctx.defer()
        try:
            msg_id = int(msg_id)
            msgObj = await ctx.channel.fetch_message(msg_id)
            await ctx.defer(hidden=True)
            await msgObj.reply(
                "https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")
        except Exception as e:
            await ctx.defer()
            await ctx.send(content="https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")

    @cog_ext.cog_slash(name="confess", description="Submits an anonymous confession", options=[create_option(name="confession", description="Opinion/confession you want to post anonymously", option_type=3, required=True)])
    async def confess(self, ctx, *, confession: str):
        await ctx.defer(hidden=True)
        banFile = open('cogs/ban_list.csv', 'r')
        memberId = str(ctx.author_id)
        banList = []
        for line in banFile:
            banList.append(line.split('\n')[0].replace('\n', ''))
        if(memberId not in banList):
            confessEmbed = discord.Embed(title="Anonymous confession", color=discord.Color.random(
            ), description=confession, timestamp=datetime.now(IST))
            dest = self.client.get_channel(860224115633160203)
            await ctx.send(f":white_check_mark: Your confession has been submitted to {dest.mention}", hidden=True)
            await dest.send(embed=confessEmbed)
            messages = await dest.history(limit=3).flatten()
            for message in messages:
                if((message.author.id == 749484661717204992) and (len(message.embeds) > 0)):
                    required_message = message
                    break
            await self.storeId(str(ctx.author_id), str(required_message.id))
        else:
            await ctx.send(":x: You have been banned from submitting anonymous confessions", hidden=True)

    async def storeId(self, memberId: str, messageId: str):
        confessions = self.confessions
        for key in confessions:
            if(key == memberId):
                confessions[key].append(messageId)
                self.confessions = confessions
                return
            else:
                continue
        confessions[memberId] = [messageId]

    @cog_ext.cog_slash(name="confessban", description="Bans a user from submitting confessions who submitted a confession based on message ID", options=[create_option(name="msg_id", description="Message ID of the confession", option_type=3, required=True)])
    async def confessban(self, ctx, msg_id: str):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await ctx.defer(hidden=True)
            confessions = self.confessions
            msg_id_str = str(msg_id)
            banFile = open('cogs/ban_list.csv', 'r')
            banList = []
            for line in banFile:
                banList.append(line.split('\n')[0].replace('\n', ''))
            banFile.close()
            banFile = open('cogs/ban_list.csv', 'a')
            for key in confessions:
                msgList = confessions[key]
                if(msg_id_str in msgList):
                    if(key not in banList):
                        banFile.write(f"{key}\n")
                        await ctx.send("Member banned succesfully", hidden=True)
                        banFile.close()
                        try:
                            dm = await self.client.fetch_user(int(key))
                            dm_embed = discord.Embed(title="Notification", description="You have been banned from submitting confessions", color=discord.Color.red())
                            await dm.send(embed=dm_embed)
                        except:
                            await ctx.send("DMs were closed", hidden=True)
                        return
                    else:
                        await ctx.send("This fellow was already banned", hidden=True)
                else:
                    continue
            await ctx.send("Could not ban", hidden=True)
            banFile.close()
        else:
            await ctx.send("You are not authorised to do this")

    @cog_ext.cog_slash(name="confessbanuser", description="Bans a user from submitting confessions", options=[create_option(name="member", description="User/Member to ban", option_type=6, required=True)])
    async def confessbanuser(self, ctx, member: discord.Member):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await ctx.defer(hidden=True)
            user_id = str(member.id)
            banFile = open('cogs/ban_list.csv', 'r')
            banList = []
            for line in banFile:
                banList.append(line.split('\n')[0].replace('\n', ''))
            banFile.close()
            if(user_id not in banList):
                banFile = open('cogs/ban_list.csv', 'a')
                banFile.write(f"{user_id}\n")
                await ctx.send("User banned succesfully", hidden=True)
                banFile.close()
                try:
                    dm = await self.client.fetch_user(int(user_id))
                    dm_embed = discord.Embed(title="Notification", description="You have been banned from submitting confessions", color=discord.Color.red())
                    await dm.send(embed=dm_embed)
                except:
                    await ctx.send("DMs were closed", hidden=True)
            else:
                await ctx.send("This user has already been banned", hidden=True)
        else:
            await ctx.send("You are not authorised for this")

    @cog_ext.cog_slash(name="confessunbanuser", description="Unbans a user from submitting confessions", options=[create_option(name="member", description="User/Member to unban", option_type=6, required=True)])
    async def confessunbanuser(self, ctx, member: discord.Member):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await ctx.defer(hidden=True)
            user_id = str(member.id)
            dat = ''
            deleted = False
            banFile = open('cogs/ban_list.csv', 'r')
            for line in banFile:
                if(user_id in line.split(',')[0].replace('\n', '')):
                    deleted = True
                    continue
                dat += line
            banFile.close()
            if(deleted):
                banFile = open('cogs/ban_list.csv', 'w')
                banFile.write(dat)
                banFile.close()
                await ctx.send("User has been unbanned successfully", hidden=True)
                try:
                    dm = await self.client.fetch_user(int(user_id))
                    dm_embed = discord.Embed(title="Notification", description="You have been unbanned from submitting confessions", color=discord.Color.green())
                    await dm.send(embed=dm_embed)
                except:
                    await ctx.send("DMs were closed", hidden=True)
            else:
                await ctx.send("This fellow was never banned in the first place", hidden=True)


@tasks.loop(hours=24)
async def flush_confessions(self):
    self.confessions = {}


def setup(client):
    client.add_cog(misc(client))
