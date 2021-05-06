import discord
from discord.ext import commands
from time import sleep
from discord.utils import get
# from verification import verification

GUILD_ID = 742797665301168220
BOT_LOGS = 786084620944146504
MOD_LOGS = 778678059879890944


class server(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.veri = '`!v` or `!verify`\n!v help\n!v {SRN}'
        self.count = '`!c` or `!count`\n!c {Role name(don\'t mention it, type it out)}\n\nReturns the number of people with the speified role'
        self.ping = '`!ping` or `!Ping`\n\nReturns the bot\'s latency'
        self.info = '`!i` or `!info`\n!i {Member mention}\n!i {Member ID}\n\nReturns the information about a verified user on this server'
        self.deverify = '`!d` or `!deverify`\n!d {Member mention}\n\nDeverifies and removes the data of the user from the verified list'
        self.fil = '`!f` or `!file`\n\nSends the verified.csv file to #bot-test'
        self.purge = '`!p` or `!purge`\n!p {amount}\n\nPurges the specified number of messages(limit=1000)'
        self.echo = '`!e` or `!echo`\n!e {Channel mention} {Text}\n\nEchoes a message through the bot to the specified channel'
        self.mute = '`!mute`\n!mute {Member mention} {Time} {Reason: optional}\n\nMutes the user for the specified time'
        self.unmute = '`!unmute`\n!unmute {Member mention}\n\nUnmutes the user'
        self.lock = '`!lock`\n!lock {Channel mention} {Reason: optional}\n\nLocks the specified channel'
        self.unlock = '`!unlock`\n!unlock {Channel mention}\n\nUnlocks the specified channel'
        self.kick = '`!kick`\n!kick {Member mention} {Reason: optional}\n\nKicks the member from the server'


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=742800061280550923)
        self.mods = get(self.guildObj.roles, id=742798158966292640)
        self.bot_devs = get(self.guildObj.roles, id=750556082371559485)
        self.just_joined = get(self.guildObj.roles, id=798765678739062804)
        self.verified = get(self.guildObj.roles, id=749683320941445250)

        await self.client.get_channel(BOT_LOGS).send("Bot is online")
        await self.client.get_channel(BOT_LOGS).send(f"Logged in as {self.client.user}")
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the PRIDE of PESU"),
        )


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # error handling, in case of an error the error message will be put up in the channel
        string = f"Something's wrong, I can feel it\n{str(error)}"
        await ctx.channel.send(string)
        await self.client.get_channel(BOT_LOGS).send(f"{string}\n{str(ctx.message.author.mention)} is a noob who made this mistake in {str(ctx.message.channel.mention)}")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.client.get_channel(BOT_LOGS).send(f"{member.name} Joined\ni.e., {str(member.mention)} just joined")
        await member.add_roles(self.just_joined)


    @commands.Cog.listener()
    async def on_member_remove(self, user):
        await self.client.get_channel(BOT_LOGS).send(f"{str(user)} just left.")
        await self.client.get_channel(BOT_LOGS).send(f"i.e., {str(user.mention)} just left")
        if(self.getDeverified(str(user.id))):
            await self.client.get_channel(BOT_LOGS).send("Deverified the user")


    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.author.bot):
            pass
        else:
            temp = message.content.replace("`", "|")
            if ('<@&781150455576789032>' in str(temp)):
                ping_log = f"{message.author.mention} pinged lawda geng in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)
            if ('<@&750556082371559485>' in str(temp)):
                ping_log = f"{message.author.mention} pinged botdev in {message.channel.mention}"            
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)
            if ('<@&742798158966292640>' in str(temp)) :
                ping_log = f"{message.author.mention} pinged mods in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)
            if ('<@&742800061280550923>' in str(temp)):
                ping_log = f"{message.author.mention} pinged admin in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)

    
    @commands.command(aliases=['h', 'help'])
    async def _help(self, ctx):
        help_embed = discord.Embed(title="PESU BOT", color=0x48BF91)
        if(self.just_joined in ctx.author.roles):
            help_embed.add_field(name="Verification", value=self.veri)
            await ctx.channel.send(embed=help_embed)
            return
        help_embed.add_field(name="Count", value=self.count)
        help_embed.add_field(name="Ping", value=self.ping)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            help_embed.add_field(name="Info", value=self.info)
            help_embed.add_field(name="Deverify", value=self.deverify)
            help_embed.add_field(name="Purge", value=self.purge)
            help_embed.add_field(name="Echo", value=self.echo)
            if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
                help_embed.add_field(name="Mute", value=self.mute)
                help_embed.add_field(name="Unmute", value=self.unmute)
                help_embed.add_field(name="Lock", value=self.lock)
                help_embed.add_field(name="Unlock", value=self.unlock)
                help_embed.add_field(name="Kick", value=self.kick)
            if((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
                help_embed.add_field(name="File", value=self.fil)
        await ctx.channel.send(embed=help_embed)


    @commands.command(aliases=['ping', 'Ping'])
    async def _ping(self, ctx):
        ps = f"Pong!!!\nPing = `{str(round(self.client.latency * 1000))} ms`"
        await ctx.channel.send(ps)


    def getDeverified(self, a=""):
        dat = ""
        ret = False
        file1 = open('cogs/verified.csv', 'r')

        for line in file1:
            if(a not in line.split(',')):
                dat += line
            else:
                ret = True

        file1.close()
        
        file1 = open('cogs/verified.csv', 'w')
        file1.write(dat)
        file1.close()

        return ret


def setup(client):
    client.add_cog(server(client))
    