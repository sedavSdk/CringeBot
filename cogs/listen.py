from discord.ext import commands
import datetime

class CogListen(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.leverId = 1155111810643542057
    
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{datetime.datetime.now()}: new picture in the levers")
        if message.channel.id == self.leverId:
            await message.add_reaction('📍')
    
    @commands.command()
    async def setId(self, ctx, id : int):
        self.leverId = id