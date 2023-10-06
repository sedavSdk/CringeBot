from discord.ext import commands
import discord
from discord import app_commands
import asyncio

class CogVoiting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.id : int = 1

    class Ful(discord.ui.View):
        class Btn(discord.ui.Button):
            def __init__(self, label, custom_id, ful, number, time=1):
                super().__init__(label=label, custom_id=custom_id)
                self.callback = self.button_callback
                self.voteNumber = 0
                self.ful = ful
                self.number = number
                self.channel = None
            
            async def button_callback(self, i):
                    if i.user.id not in self.ful.users:
                        self.ful.vouts[self.number] += 1
                        self.ful.users[i.user.id] = 1
                    await i.response.edit_message(embed=self.ful.getContent()[1])

        def __init__(self, theme, id, args=[]):
            super().__init__()
            self.args = args
            self.id = id
            self.heading = theme
            self.content = [""] * 7
            self.vouts = [0] * 7
            self.circles = ["🔵", "🔴", "🟢", "🟠", "🟣", "🟤", "🟡"]
            self.tcircles = ["1️⃣", "2️⃣", "3️⃣", "🟤", "🟤", "🟤", "🟤"]
            self.users = {}
            self.colour = discord.Colour.from_rgb(173, 255, 47)

            for i in range(0, len(args)):
                if args[i]!="pipipoopoo":
                    self.content[i] = self.args[i]
                    b = self.Btn(label= self.circles[i] + args[i], custom_id=str(self.id), ful=self, number=i)
                    self.add_item(b)
                    self.id += 1
            
        def getContent(self):
            c = self.heading + "\n"
            str = ""
            for i in range(0, len(self.content)):
                if len(self.content[i]) > 0:
                    str = str + "\n" + self.circles[i] + f' `{self.vouts[i]}` - ' + self.content[i]
            c2 = discord.Embed(color=self.colour, description=str, title=c)
            return [c, c2]
        
    async def kill(self, thing_for_del, timeH, timeM, interaction: discord.Interaction):
        print(f"start timer, vote created by {interaction.user}, expired in {timeH} hours and {timeM} minutes")
        await asyncio.sleep(timeH*3600 + timeM*60)
        await thing_for_del.channel.send(embed=thing_for_del.getContent()[1], content="Голосование завершено")
        for i in thing_for_del.children:
            del i.callback
            del i
        del thing_for_del

        

        
    
    @app_commands.command(name="vote", description="Создаёт голосование")
    @app_commands.describe(time_hours="Количество часов, которые просуществует голосование (0 по умочанию)")
    @app_commands.describe(time_min="Количество минут, которые просуществует голосование (10 по умочанию)")
    @app_commands.describe(var1="Вариант ответа в голосовании")
    @app_commands.describe(var2="Вариант ответа в голосовании")
    @app_commands.describe(var3="Вариант ответа в голосовании")
    @app_commands.describe(var4="Вариант ответа в голосовании")
    @app_commands.describe(var5="Вариант ответа в голосовании")
    @app_commands.describe(var6="Вариант ответа в голосовании")
    @app_commands.describe(var7="Вариант ответа в голосовании")
    @app_commands.describe(theme="Тема голосования")
    async def createVote(self, interaction: discord.Interaction, theme : str, var1 : str, var2: str, time_hours : int = 0, time_min : int = 10, var3: str="pipipoopoo", var4: str="pipipoopoo", var5: str="pipipoopoo", var6: str="pipipoopoo", var7: str="pipipoopoo"):
        args = [var1, var2, var3, var4, var5, var6, var7]
        view = self.Ful(theme, self.id, args)
        self.id = view.id
        view.channel = interaction.channel
        #await view.kill(time)
        await interaction.response.send_message(embed=view.getContent()[1], view=view, delete_after=time_hours * 3600 + time_min * 60)
        await self.kill(view, time_hours, time_min, interaction)
    
    @commands.Cog.listener()
    async def on_button_click(interaction):
        id = interaction.custom_id
        await interaction.respond(content={id})