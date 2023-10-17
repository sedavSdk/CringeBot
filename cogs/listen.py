from discord.ext import commands
import datetime
import configparser
import sys
sys.path.append("..")
from utils import doImage
import discord
from random import choice

class CogListen(commands.Cog):
    def __init__(self, client):
        self.client = client
        config = configparser.ConfigParser()
        config.read('cogs.ini')

        self.leverId = config['id']['lever_id']

        self.systemId = config.getint('id', 'system_id')
        self.logovoId = config.getint('id', 'guild_id')
        self.logovo = None
        self.system = None
        self.testId = config.getint('id', 'test_id')
        self.test = None
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.leverId:
            print(f"{datetime.datetime.now()}: new picture in the levers")
            await message.add_reaction('📍')
    
    @commands.command()
    async def setId(self, ctx, id : int):
        self.leverId = id
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.logovo = self.client.get_guild(self.logovoId)
        self.system = discord.utils.get(self.logovo.channels, id=self.systemId)
        self.test = discord.utils.get(self.logovo.channels, id=self.testId)
    
    @commands.Cog.listener()
    async def on_member_remove(self, mem):
        m=[" покинул нас...", " ушел и больше не вернулся", " нашел себе сервер получше", "съебал нахуй"]
        await self.system.send(content=f'{mem.global_name} {choice(m)}')
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            new_role = next(role for role in after.roles if role not in before.roles)
            if new_role.name in ('Логовичанин'):

                url = after.avatar.url
                doImage(url)
                with open('результат.png', 'rb') as f:
                    picture = discord.File(f)
                    await self.test.send(file=picture)