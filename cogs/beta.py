import discord
from discord.ext import commands, tasks
# from discord.utils import get
import os
from dotenv import load_dotenv
import asyncio
import base64
from datetime import datetime
from selenium import webdriver

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = 742797665301168220

ANNOUNCEMENTS = 810508395546542120

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
PESU_SRN=os.getenv('SRN')
PESU_PWD=os.getenv('PWD')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

TODAY_ANNOUNCEMENTS_MADE = list()
ALL_ANNOUNCEMENTS_MADE = list() 


class beta(commands.Cog):

    # slash = SlashCommand(commands.bot)
    def __init__(self, client):
        self.client = client
        # slash = SlashCommand(self.client, sync_commands = True)
        self.checkPESUAnnouncement.start()
        self.checkNewDay.start()
        

    # This file will be used for obsolete code(if needed to be stored) or any other function
    # to be tested before moving to another cog


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)

    #     self.admin = get(self.guildObj.roles, id=742800061280550923)
    #     self.bot_devs = get(self.guildObj.roles, id=750556082371559485)


    # def run(*args):
    #     # return os.system('git commit')
    #     return os.system("git " + " ".join(list(args)))


    # def pull():
    #     run("pull", "origin", "master")


    # def commit():

    #     commit_message = "Bot Updating verified.csv"
    #     run("pull")
    #     run("commit", "-m", commit_message)
    #     run("push")


    # @commands.command(aliases=['u', 'update'])
    # async def _update(self, ctx):
    #     if((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
    #         pull()
    #         commit()
    #         await ctx.channel.send("You updated to git repo")
    #     else:
    #         await ctx.channel.send("You are not authorised to do that")

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
                    print(attachment_names)
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

        print(f"Announcements TODAY: {len(TODAY_ANNOUNCEMENTS_MADE)}")
        print(f"Announcements ALL: {len(ALL_ANNOUNCEMENTS_MADE)}")

        announcements = ALL_ANNOUNCEMENTS_MADE
        N = len(ALL_ANNOUNCEMENTS_MADE)
        if query != None:
            filters = query.lower().split()[:2]
            for f in filters:
                if f == "today":
                    announcements = TODAY_ANNOUNCEMENTS_MADE
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

        print("Fetching announcements...")
        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        all_announcements = await self.getPESUAnnouncements(driver, PESU_SRN, PESU_PWD)
        print(f"Fetched announcements: {len(all_announcements)}")

        for a in all_announcements:
            if a not in ALL_ANNOUNCEMENTS_MADE:
                ALL_ANNOUNCEMENTS_MADE.append(a)
        print(f"All announcements found: {len(ALL_ANNOUNCEMENTS_MADE)}")
        ALL_ANNOUNCEMENTS_MADE.sort(key=lambda x: x["date"], reverse=True)

        current_date = datetime.now().date()
        channel = self.client.get_channel(ANNOUNCEMENTS)
        for announcement in all_announcements:
            if announcement["date"] == current_date:
                if announcement not in TODAY_ANNOUNCEMENTS_MADE:
                    await channel.send("@everyone")
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

                    print("Sending announcement...")
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

        print("Checking for new day...")
        current_time = datetime.now()
        if current_time.hour == 0:  # and current_time.minute == 0:
            print("Resetting today's announcements...")
            TODAY_ANNOUNCEMENTS_MADE = list()
            ALL_ANNOUNCEMENTS_MADE = list()
        print(f"Announcements TODAY: {len(TODAY_ANNOUNCEMENTS_MADE)}")
        print(f"Announcements ALL: {len(ALL_ANNOUNCEMENTS_MADE)}")


def setup(client):
    client.add_cog(beta(client))