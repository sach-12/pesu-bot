import discord
from discord.ext import commands, tasks
from time import sleep
import os
import asyncio
from dotenv import load_dotenv
import base64
from discord.utils import get
from datetime import datetime
from selenium import webdriver
from pathlib import Path

GUILD_ID = 742797665301168220
BOT_LOGS = 786084620944146504
MOD_LOGS = 778678059879890944
ANNOUNCEMENTS = 749628212782563368

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
PESU_SRN=os.getenv('SRN')
PESU_PWD=os.getenv('PASSWD')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

TODAY_ANNOUNCEMENTS_MADE = list()
ALL_ANNOUNCEMENTS_MADE = list() 



class server(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.veri = '`!v` or `!verify`\n!v help\n!v {SRN}'
        self.count = '`!c` or `!count`\n!c {Role name(don\'t mention it, type it out)}\n\nReturns the number of people with the speified role'
        self.ping = '`!ping` or `!Ping`\n\nReturns the bot\'s latency'
        self.news = '`!news [optional]`\n\nPESU Academy Notifications\nUsage:\n`!news`: Gets the latest announcement\n`!news today`: Gets today\'s announcements\n`!news {N}`: Gets the last "N" announcements(where N is a number)\n`!news today {N}`: Gets last "N" announcements made today\n`!news all`: Gets all announcements(max: 10)'
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

        self.checkPESUAnnouncement.start()
        self.checkNewDay.start()


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=742800061280550923)
        self.mods = get(self.guildObj.roles, id=742798158966292640)
        self.bot_devs = get(self.guildObj.roles, id=750556082371559485)
        self.budday = get(self.guildObj.roles, id=842294715415396383)
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
    async def on_member_update(self, before, after):
        if((self.budday not in before.roles) and (self.budday in after.roles)):
            await self.client.get_channel(798472825589334036).send(f"Yo, it's {before.mention}'s birthday!")


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
        help_embed.add_field(name="News", value=self.news)
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


    async def getPESUAnnouncements(self, chrome, username, password):
        chrome.get("https://pesuacademy.com/Academy")
        await asyncio.sleep(2)

        username_box = chrome.find_element_by_xpath(r'//*[@id="j_scriptusername"]')
        password_box = chrome.find_element_by_xpath(r'//*[@name="j_password"]')

        username_box.send_keys(username)
        await asyncio.sleep(0.3)
        password_box.send_keys(password)
        await asyncio.sleep(0.3)

        sign_in_button = chrome.find_element_by_xpath(
            r'//*[@id="postloginform#/Academy/j_spring_security_check"]')
        sign_in_button.click()
        await asyncio.sleep(1)

        menu_options = chrome.find_elements_by_xpath(r'//*[@class="menu-name"]')
        menu_options[8].click()
        await asyncio.sleep(1)

        announcement_boxes = chrome.find_elements_by_xpath(
            r'//*[@class="elem-info-wrapper"]')
        announcement_boxes.extend(chrome.find_elements_by_xpath(
            r'//*[@class="elem-info-wrapper  "]'))

        data = list()
        for a_box in announcement_boxes:
            header_box = a_box.find_element_by_xpath(r'.//*[@class="text-info"]')
            header = header_box.text

            date_box = a_box.find_element_by_xpath(
                r'.//*[@class="text-muted text-date pull-right"]')
            date = datetime.strptime(date_box.text, "%d-%B-%Y").date()

            bodies = a_box.find_elements_by_xpath(r'.//*[@class="col-md-12"]')
            all_attachments = list()
            if not bodies:
                bodies = a_box.find_elements_by_xpath(r'.//*[@class="col-md-8"]')
            for b in bodies:
                paragraphs = b.find_elements_by_tag_name("p")
                attachments = b.find_elements_by_xpath(
                    r'.//*[@class="pesu-ico-download"]')
                attachment_names = b.find_elements_by_tag_name("a")
                if paragraphs:
                    content = '\n'.join([p.text for p in paragraphs])
                if attachments:
                    attachment_names = [
                        a_name.text for a_name in attachment_names if a_name.text != "Read more"]
                    all_attachments.extend(attachment_names)
                    for a in attachments:
                        a.click()

            img_base64 = None
            img_box = a_box.find_elements_by_xpath(
                r'.//*[@class="img-responsive"]')
            if img_box:
                img_base64 = img_box[0].get_attribute("src")

            temp = {
                "date": date,
                "header": header,
                "body": content,
                "img": img_base64,
                "attachments": all_attachments
            }

            data.append(temp)

        return data

    @commands.command(aliases=["news"])
    async def pesunews(self, ctx, *, query=None):
        global TODAY_ANNOUNCEMENTS_MADE
        global ALL_ANNOUNCEMENTS_MADE


        announcements = ALL_ANNOUNCEMENTS_MADE
        N = 1
        if query != None:
            filters = query.lower().split()[:2]
            for f in filters:
                if f == "today":
                    announcements = TODAY_ANNOUNCEMENTS_MADE
                else:
                    if f == "all":
                        N = len(ALL_ANNOUNCEMENTS_MADE)
                    else:
                        try:
                            temp_limit = int(f)
                            N = temp_limit
                        except ValueError:
                            pass
        announcements = announcements[:N]

        if announcements:
            for announcement in announcements:
                title = announcement["header"]
                if len(title) > 256:
                    embed = discord.Embed(title=title[:253] + "...", description="..." +
                                        title[253:], color=0x03f8fc)
                else:
                    embed = discord.Embed(
                        title=title, color=0x03f8fc)

                content_body = str(announcement["body"])
                if len(content_body) > 1024:
                    content_bodies = content_body.split('\n')
                    content_bodies = [c for c in content_bodies if c.strip() not in [
                        "", " "]]
                    for i, c in enumerate(content_bodies):
                        if i == 0:
                            embed.add_field(
                                name=str(announcement["date"]), value=c, inline=False)
                        else:
                            embed.add_field(name=f"\u200b", value=c, inline=False)
                else:
                    embed.add_field(
                        name=str(announcement["date"]), value=content_body)

                if announcement["img"] != None:
                    img_base64 = announcement["img"].strip()[22:]
                    imgdata = base64.b64decode(img_base64)
                    filename = "announcement-img.png"
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    with open(filename, 'rb') as f:
                        img_file = discord.File(f)
                        await ctx.send(file=img_file)

                await ctx.send(embed=embed)
                if announcement["attachments"]:
                    for fname in announcement["attachments"]:
                        attachment_file = discord.File(fname)
                        await ctx.send(file=attachment_file)
        else:
            await ctx.send("No announcements available. Retry with another option or try again later.")


    @tasks.loop(minutes=5)
    async def checkPESUAnnouncement(self):
        global TODAY_ANNOUNCEMENTS_MADE
        global ALL_ANNOUNCEMENTS_MADE
        await self.client.wait_until_ready()

        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        all_announcements = await self.getPESUAnnouncements(driver, PESU_SRN, PESU_PWD)

        for a in all_announcements:
            if a not in ALL_ANNOUNCEMENTS_MADE:
                ALL_ANNOUNCEMENTS_MADE.append(a)
        ALL_ANNOUNCEMENTS_MADE.sort(key=lambda x: x["date"], reverse=True)

        current_date = datetime.now().date()
        channel = self.client.get_channel(ANNOUNCEMENTS)
        for announcement in all_announcements:
            if announcement["date"] == current_date:
                if announcement not in TODAY_ANNOUNCEMENTS_MADE:
                    title = announcement["header"]
                    if len(title) > 256:
                        embed = discord.Embed(title=title[:253] + "...", description="..." +
                                            title[253:], color=0x03f8fc)
                    else:
                        embed = discord.Embed(
                            title=title, color=0x03f8fc)

                    content_body = str(announcement["body"])
                    if len(content_body) > 1024:
                        content_bodies = content_body.split('\n')
                        content_bodies = [c for c in content_bodies if c.strip() not in [
                            "", " "]]
                        for i, c in enumerate(content_bodies):
                            if i == 0:
                                embed.add_field(
                                    name=str(announcement["date"]), value=c, inline=False)
                            else:
                                embed.add_field(
                                    name=f"\u200b", value=c, inline=False)
                    else:
                        embed.add_field(
                            name=str(announcement["date"]), value=content_body)

                    if announcement["img"] != None:
                        img_base64 = announcement["img"].strip()[22:]
                        imgdata = base64.b64decode(img_base64)
                        filename = "announcement-img.png"
                        with open(filename, 'wb') as f:
                            f.write(imgdata)
                        with open(filename, 'rb') as f:
                            img_file = discord.File(f)
                            await channel.send(file=img_file)

                    await self.client.get_channel(BOT_LOGS).send("Sending announcement...")
                    await channel.send(embed=embed)
                    if announcement["attachments"]:
                        for fname in announcement["attachments"]:
                            attachment_file = discord.File(fname)
                            await channel.send(file=attachment_file)
                    TODAY_ANNOUNCEMENTS_MADE.append(announcement)
        driver.quit()


    @tasks.loop(minutes=10)
    async def checkNewDay(self):
        global TODAY_ANNOUNCEMENTS_MADE
        global ALL_ANNOUNCEMENTS_MADE
        await self.client.wait_until_ready()

        current_time = datetime.now()
        if current_time.hour == 0:  # and current_time.minute == 0:
            TODAY_ANNOUNCEMENTS_MADE = list()
            ALL_ANNOUNCEMENTS_MADE = list()
            await self.cleanUp()

    
    async def cleanUp(self):
        files = [fname for fname in os.listdir() if Path(fname).suffix in [".pdf", ".png", ".jpg", ".jpeg"]]
        for fname in files:
            try:
                os.remove(fname)
            except FileNotFoundError:
                pass


def setup(client):
    client.add_cog(server(client))
    