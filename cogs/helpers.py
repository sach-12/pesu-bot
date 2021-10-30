import discord
from discord.ext import commands


class helpers(commands.Cog):


    def __init__(self, client):
        self.client = client


    def getuser(self, RegNo=""):
        if(RegNo == ""):
            return['error']
        f = open('cogs/verified.csv', 'r')
        srn_list = [line.split(',')[3] for line in list(filter(None, f.read().split('\n')))]
        if(RegNo in srn_list):
            f.close()
            return ['Done']
        f.close()
        file = None
        if ('PES12018' in RegNo or 'PES22018' in RegNo):
            file = open('cogs/batch_list_2018.csv', 'r')
        elif ('PES1UG19' in RegNo or 'PES2UG19' in RegNo):
            file = open('cogs/batch_list_2019.csv', 'r')
        elif ('PES1UG20' in RegNo or 'PES2UG20' in RegNo):
            file = open('cogs/batch_list_2020.csv', 'r')
        # elif ('PES1UG21' in a):
        elif ('PES12021' in RegNo or 'PES22021' in RegNo):
            file = open('cogs/batch_list_2021.csv', 'r')

        if file == None:
            return ['no match']
        for lin in file:
            if(RegNo in lin):
                f.close()
                return lin.split(',')
        
        file.close()
        return ['error']


    def getDeverified(self, regNo=""):
        dat = ""
        ret = False
        file1 = open('cogs/verified.csv', 'r')

        for line in file1:
            if(regNo not in line.split(',')):
                dat += line
            else:
                ret = True

        file1.close()
        
        file1 = open('cogs/verified.csv', 'w')
        file1.write(dat)
        file1.close()

        return ret


    def getVerified(self, a=""):
        if(a == ""):
            return ['unverified']
        file = open('cogs/verified.csv', 'r')

        for line in file:
            line = line.split(',')
            if(len(line) > 5):
                if(a == line[1]):
                    file.close()
                    return line
        file.close()
        return ['unverified']


def setup(client):
    client.add_cog(helpers(client))