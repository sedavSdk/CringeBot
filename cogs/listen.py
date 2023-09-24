from discord.ext import commands

class CogListen(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.leverId = 1155111810643542057
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.leverId:
            await message.add_reaction('📍')
    
    @commands.command()
    async def setId(self, ctx, id : int):
        self.leverId = id