import discord
from discord.ext import commands
from time import sleep
from discord.utils import get
import asyncio

GUILD_ID = 742797665301168220
MOD_LOGS = 778678059879890944


class misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=742800061280550923)
        self.mods = get(self.guildObj.roles, id=742798158966292640)
        self.bot_devs = get(self.guildObj.roles, id=750556082371559485)
        self.bots = get(self.guildObj.roles, id=746226955094851657)
        self.muted = get(self.guildObj.roles, id=775981947079491614)
        self.purge = '`!p` or `!purge`\n!p {amount}\nPurges the specified number of messages(limit=1000)'
        self.echo = '`!e` or `!echo`\n!e {Channel mention} {Text}\n Echoes a message through the bot to the specified channel'
        self.mute = '`!mute`\n!mute {Member mention} {Time} {Reason: optional}\nMutes the user for the specified time'
        self.unmute = '`!unmute`\n!unmute {Member mention}\nUnmutes the user'
        self.lock = '`!lock`\n!lock {Channel mention} {Reason: optional}\nLocks the specified channel'
        self.unlock = '`!unlock`\n!unlock {Channel mention}\nUnlocks the specified channel'
        self.kick = '`!kick`\n!kick {Member mention} {Reason: optional}\nKicks the member from the server'


    @commands.command(aliases=['c', 'count'])
    async def _count(self, ctx, *roleName):
        roleName = ' '.join(roleName)
        # convert it back into string and split it at '&' and strip the individual roles.
        try:
            roleName = roleName.split('&')
        except:
            pass
        temp =[]
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
        purge_embed = discord.Embed(title="Purge", color=0x48BF91, desciption=self.purge)
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
    async def _echo(self, ctx, *message):
        echo_embed = discord.Embed(title="Echo", color=0x48BF91, desciption=self.echo)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            try:
                message = list(message)
                url = message[0].url
                channel = message[0]
                message = message[1:]
            except Exception as e:
                await ctx.channel.send(f"Lawda I'm getting this:\n{str(e)}", embed=echo_embed)
                return
            channel = str(channel)
            newChannel = ''
            for i in channel:
                if(i in "0123456789"):
                    newChannel += i
                message = ' '.join(message)
                newChannel = int(newChannel)
                if(newChannel == ctx.channel.id):
                    await ctx.channel.purge(limit=1)
                await self.client.get_channel(newChannel).send(message,url = message.url)
        else:
            await ctx.channel.send("Sucka you can't do that")


    @commands.command(aliases=['mute'])
    async def _mute(self, ctx, member, time, *reason):
        mute_help_embed = discord.Embed(title="Mute", color=0x48BF91, description=self.mute)

        reason=list(reason)
        reason=" ".join(reason)
        if (reason==""):
            reason = "no reason given"
        
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if('@' in str(member)):
                member = str(member)
                id = ''
                for i in member:
                    if(i in '1234567890'):
                        id += i
                member = int(id) #get their id
                member = ctx.message.guild.get_member(member)
                
                seconds=0
                if(time.lower().endswith("d")):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                if(time.lower().endswith("h")):
                    seconds += int(time[:-1]) * 60 * 60
                elif(time.lower().endswith("m")):
                    seconds += int(time[:-1]) * 60
                elif(time.lower().endswith("s")):
                    seconds += int(time[:-1])
                
                if((seconds <= 0) or (seconds > 2592000)):
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
                            mute_embed = discord.Embed(title="Mute", color=0xff0000)
                            mute_user = f"{member.mention} was muted"
                            mute_embed.add_field(name="Muted user", value=mute_user)
                            await ctx.channel.send(embed=mute_embed)
                            mute_embed_logs = discord.Embed(title="Mute", color=0xff0000)
                            mute_details_logs = f"{member.mention}\t Time: {time}\n Reason: {reason}\n Moderator: {ctx.author.mention}"
                            mute_embed_logs.add_field(name="Muted user", value=mute_details_logs)
                            await self.client.get_channel(MOD_LOGS).send(embed=mute_embed_logs)
                            await asyncio.sleep(seconds)
                            if(self.muted in member.roles):
                                unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
                                unmute_user = f"{member.mention} welcome back"
                                unmute_embed.add_field(name="Unmuted user", value=unmute_user)
                                await ctx.channel.send(embed=unmute_embed)
                                unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
                                unmute_details_logs = f"{member.mention}\n Moderator: Auto"
                                unmute_embed_logs.add_field(name="Unmuted user", value=unmute_details_logs)
                                await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                                await member.remove_roles(self.muted)
            else:
                await ctx.channel.send(f"{ctx.author.mention}, mention the user, not just the name", embed=mute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")


    @commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, member: discord.Member):
        unmute_help_embed = discord.Embed(title="Unmute", color=0x48BF91, description=self.unmute)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            try:
                if(self.muted not in member.roles):
                    await ctx.channel.send("Lawda he's not muted only means")
                else:
                    unmute_embed = discord.Embed(title="Unmute", color=0x00ff00)
                    unmute_user = f"{member.mention} welcome back"
                    unmute_embed.add_field(name="Unmuted user", value=unmute_user)
                    await ctx.channel.send(embed=unmute_embed)
                    unmute_embed_logs = discord.Embed(title="Unmute", color=0x00ff00)
                    unmute_details_logs = f"{member.mention}\n Moderator: {ctx.author.mention}"
                    unmute_embed_logs.add_field(name="Unmuted user", value=unmute_details_logs)
                    await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                    await member.remove_roles(self.muted)
            except:
                await ctx.channel.send(embed=unmute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")


    @commands.command(aliases=['lock'])
    async def _lock_channel(self, ctx, channel, *reason):
        lock_help_embed = discord.Embed(title="Embed", color=0x48BF91, description=self.lock)

        reason = list(reason)
        reason = ' '.join(reason)
        if(reason == ''):
            reason = 'no reason given'

        overwrites = discord.PermissionOverwrite(send_messages=False, view_channel=False)
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
            lock_embed = discord.Embed(title="Channel Locked :lock:", color=0xff0000, description=reason)
            await channelObj.send(embed=lock_embed)
            lock_message = discord.Embed(title="", color=0x00ff00, description = f"Locked {channelObj.mention}")
            await ctx.channel.send(embed=lock_message)
            lock_logs = discord.Embed(title="Lock", color=0xff0000)
            lock_logs.add_field(name="Channel", value=channelObj.mention)
            lock_logs.add_field(name="Moderator", value=ctx.author.mention)
            await self.client.get_channel(MOD_LOGS).send(embed=lock_logs)
        else:
            await ctx.channel.send("Lawda, I am not dyno to let you do this")


    @commands.command(aliases=['unlock'])
    async def _unlock_channel(self, ctx, channel):
        unlock_help_embed = discord.Embed(title="Unlock", color=0x48BF91, description=self.unlock)
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
                unlock_embed = discord.Embed(title="Channel Unlocked :unlock:", color=0x00ff00)
                await channelObj.send(embed=unlock_embed)
                unlock_message = discord.Embed(title="", color=0x00ff00, description = f"Unlocked {channelObj.mention}")
                await ctx.channel.send(embed=unlock_message)
                unlock_logs = discord.Embed(title="Unlock", color=0x00ff00)
                unlock_logs.add_field(name="Channel", value=channelObj.mention)
                unlock_logs.add_field(name="Moderator", value=ctx.author.mention)
                await self.client.get_channel(MOD_LOGS).send(embed=unlock_logs)
            else:
                await ctx.send("Lawda that channel is already unlocked")
        else:
            await ctx.channel.send("Lawda, I am not dyno to let you do this")

    @commands.command(aliases = ['contribute', 'support'])
    async def _support(self, ctx, *params):
        Embeds = discord.Embed(title="Contributions", color=0x00ff00)
        Embeds.add_field(name="Github repo", value="https://github.com/sach-12/pesu-bot",inline = False)
        Embeds.add_field(name = '\u200b', value ="If you wish to contribute to the bot, run these steps:",inline = False)
        rules = {
            0: "Pull the latest main branch, dont start working with any deprecated versions",
                
            1: "Create a new branch called `beta-(discord-username)`",

            2: "Do whatever changes you wish to do and create a pull request with the following information furnished in the request message: 'The cog you wish to change | What did you change'",

            3: "Wait for approval for reviewers. Your PR may be directly accepted or requested for further changes.",

        }
        for ruleNo in rules:
            Embeds.add_field(name = '\u200b', value ="`" + str(ruleNo) + '`: ' +  rules[ruleNo],inline = False)
        
        stark = ctx.guild.get_member(718845827413442692).mention
        flabby = ctx.guild.get_member(467341580051939339).mention
        e11i0t = ctx.guild.get_member(621283810926919680).mention
        sach = ctx.guild.get_member(723377619420184668).mention
        Embeds.add_field(name = "Reviewers", value = "`ArvindAROO` - {}\n `Flab-E` - {}\n `Mre11i0t` - {} and\n `sach-12` - {}".format(stark, flabby, e11i0t,sach), inline = False)
        Embeds.add_field(name = "Important", value = "**Under no circumstances is anyone allowed to merge to the main branch.**",inline = False)
        await ctx.send(embed=Embeds)

    @commands.command(aliases=['kick'])
    async def _kick(self, ctx, member, *reason):
        kick_help_embed = discord.Embed(title="Kick", color=0x48BF91, desciption=self.kick)

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
                kick_embed = discord.Embed(title="", color=0xff0000, description=f"{member.mention}** was kicked**")
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


def setup(client):
    client.add_cog(misc(client))
