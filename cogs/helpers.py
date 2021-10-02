import discord
from discord.ext import commands


class helpers(commands.Cog):


    def __init__(self, client):
        self.client = client


    def getuser(self, a=""):
        if(a == ""):
            return['error']
        f = open('cogs/verified.csv', 'r')
        srn_list = [line.split(',')[3] for line in list(filter(None, f.read().split('\n')))]
        if(a in srn_list):
            f.close()
            return ['Done']
        f.close()

        if ('PES12018' in a):
            file = open('cogs/batch_list_2018.csv', 'r')
        elif ('PES12019' in a):
            file = open('cogs/batch_list_2019.csv', 'r')
        elif ('PES12020' in a):
            file = open('cogs/batch_list_2020.csv', 'r')
        elif ('PES12021' in a):
            file = open('cogs/batch_list_2021.csv', 'r')

        for lin in file:
            if(a in lin):
                f.close()
                return lin.split(',')
        
        file.close()
        return ['error']


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