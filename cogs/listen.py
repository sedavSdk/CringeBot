from discord.ext import commands
import datetime

class CogListen(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.leverId = 738030257319444500
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.leverId:
            print(f"{datetime.datetime.now()}: new picture in the levers")
            await message.add_reaction('📍')
    
    @commands.command()
    async def setId(self, ctx, id : int):
        self.leverId = id