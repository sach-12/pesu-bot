import discord
from discord.ext import commands
import os
from time import sleep
from discord.utils import get

BOT_LOGS = 786084620944146504
GUILD_ID = 742797665301168220


class verification(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data_list = [
            'PRN',
            'SRN',
            'Semester',
            'Section',
            'Cycle',
            'Stream/Campus',
            'Stream',
            'Campus',
        ]


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=742800061280550923)
        self.mods = get(self.guildObj.roles, id=742798158966292640)
        self.bot_devs = get(self.guildObj.roles, id=750556082371559485)
        self.verified = get(self.guildObj.roles, id=749683320941445250)


    def getuser(self, a=""):
        if(a == ""):
            return['error']
        f = open('verified.csv', 'r')
        srn_list = [line.split(',')[3] for line in list(filter(None, f.read().split('\n')))]
        if(a in srn_list):
            f.close()
            return ['Done']
        f.close()

        if('PES12018' in a):
            file = open('batch_2018.csv', 'r')
        else:
            file = open('batch_list.csv', 'r')

        for lin in file:
            if(a in lin):
                f.close()
                return lin.split(',')
        
        file.close()
        return ['error']


    def getDeverified(self, a=""):
        dat = ""
        ret = False
        file1 = open('verified.csv', 'r')

        for line in file1:
            if(a not in line.split(',')):
                dat += line
            else:
                ret = True

        file1.close()
        
        file1 = open('verified.csv', 'w')
        file1.write(dat)
        file1.close()

        return ret


    def getVerified(self, a=""):
        if(a == ""):
            return ['unverified']
        file = open('verified.csv', 'r')

        for line in file:
            line = line.split(',')
            if(len(line) > 5):
                if(a == line[1]):
                    file.close()
                    return line
        file.close()
        return ['unverified']
        