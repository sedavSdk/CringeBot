from discord.ext import commands
import discord
import datetime
from discord import app_commands
import asyncio
import configparser
from random import choice
import time

#da

class CogVoiting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.id : int = 1

        self.config = configparser.ConfigParser()
        self.config.read('cogs.ini')
        self.voteChannel = self.config.getint('id', 'vote_chennel_id')


    class Ful(discord.ui.View):
        class Btn(discord.ui.Button):
            def __init__(self, label, custom_id, ful, number):
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
        
        class BtnRevote(discord.ui.Button):
            def __init__(self, custom_id, ful):
                super().__init__(label="🔄 Переголосовать", custom_id=str(custom_id) + "revote")
                self.ful = ful
                self.callback = self.button_callback
                self.style = discord.ButtonStyle.blurple
            
            async def button_callback(self, i):
                if i.user.id not in self.ful.users:
                    await i.response.send_message(content=f"Проголосуй сначала", ephemeral=True)
                else:
                    role = discord.utils.get(i.guild.roles, name="Переголосовавший")
                    if role not in i.user.roles:
                        await i.user.add_roles(role)
                        m = ["может вообще не будешь голосовать?", "может ну его нахуй вообще?", "может съебёшься с канала?"]
                        await self.ful.boardOfShame.send(f"{i.user.mention} если ты с первого раза не можешь нормально проголосовать, {choice(m)}")
                    await i.response.send_message(content=f"Ищи себя на доске позора {self.ful.boardOfShame.mention}", ephemeral=True)

        def __init__(self, theme, id, config, guild, time_hour, time_minute, args=[]):
            super().__init__()
            self.args = args
            self.id = id
            self.heading = theme
            self.content = [""] * 7
            self.vouts = [0] * 7
            self.circles = ["🟢", "🟠", "🟣", "🟤", "🟡", "🔵", "🔴"]
            self.users = {}
            self.colour = discord.Colour.from_rgb(173, 255, 47)
            self.boardOfShameId = config.getint('id', 'board_of_shame_id')
            self.boardOfShame = discord.utils.get(guild.channels, id=self.boardOfShameId)
            self.message_time = datetime.datetime.now()
            self.time_hour = time_hour
            self.time_minute = time_minute
            self.timeout = None

            for i in range(0, len(args)):
                if args[i]!="pipipoopoo":
                    self.content[i] = self.args[i]
                    b = self.Btn(label= self.circles[i] + ' ' + args[i], custom_id=str(self.id), ful=self, number=i)
                    self.add_item(b)
                    self.id += 1
            self.add_item(self.BtnRevote(custom_id=self.id, ful=self))
            
        def getContent(self):
            c = self.heading + "\n"
            str = "" 
            for i in range(0, len(self.content)):
                if len(self.content[i]) > 0:
                    str += "\n" + "`" + self.circles[i] + f' {self.vouts[i]}` - ' + self.content[i]
            str += "\n\nГолосование завершится " + f'<t:{int(time.mktime(self.message_time.timetuple()) + self.time_hour * 3600 + self.time_minute * 60)}:R>'
            c2 = discord.Embed(color=self.colour, description=str, title=c)
            return [c, c2]
        
        def getContentNoTimer(self):
            c = self.heading + "\n"
            str = "" 
            for i in range(0, len(self.content)):
                if len(self.content[i]) > 0:
                    str += "\n" + "`" + self.circles[i] + f' {self.vouts[i]}` - ' + self.content[i]
            c2 = discord.Embed(color=self.colour, description=str, title=c)
            return [c, c2]
        
    async def kill(self, thing_for_del, timeH, timeM, interaction: discord.Interaction):
        print(f"{datetime.datetime.now()}: start timer, vote created by {interaction.user}, expired in {timeH} hours and {timeM} minutes")
        await asyncio.sleep(timeH*3600 + timeM*60)
        await thing_for_del.channel.send(embed=thing_for_del.getContentNoTimer()[1], content="✅ Голосование завершено")
        for i in thing_for_del.children:
            del i.callback
            del i
        del thing_for_del

        

        
    
    @app_commands.command(name="vote", description="Создаёт голосование")
    @app_commands.describe(time_hours="Количество часов, которые просуществует голосование (0 по умочанию)")
    @app_commands.describe(time_min="Количество минут, которые просуществует голосование (10 по умочанию)")
    @app_commands.describe(variant1="Вариант ответа в голосовании")
    @app_commands.describe(variant2="Вариант ответа в голосовании")
    @app_commands.describe(variant3="Вариант ответа в голосовании")
    @app_commands.describe(variant4="Вариант ответа в голосовании")
    @app_commands.describe(variant5="Вариант ответа в голосовании")
    @app_commands.describe(variant6="Вариант ответа в голосовании")
    @app_commands.describe(variant7="Вариант ответа в голосовании")
    @app_commands.describe(theme="Тема голосования")
    async def createVote(self, interaction: discord.Interaction, theme : str, variant1 : str, variant2: str, time_hours : int = 0, time_min : int = 10, variant3: str="pipipoopoo", variant4: str="pipipoopoo", variant5: str="pipipoopoo", variant6: str="pipipoopoo", variant7: str="pipipoopoo"):
        if interaction.channel_id == self.voteChannel:
            if time_hours > 24:
                time_hours = 24
            if time_hours < 0:
                time_hours = 0
            if time_min > 59:
                time_min = 59
            if time_min < 1:
                if time_hours > 0:
                    time_min = 0
                else:
                    time_min = 1
            args = [variant1, variant2, variant3, variant4, variant5, variant6, variant7]
            view = self.Ful(theme, self.id, self.config, interaction.guild, time_hours, time_min, args)
            self.id = view.id
            view.channel = interaction.channel
            await interaction.response.send_message(embed=view.getContent()[1], view=view, delete_after=time_hours * 3600 + time_min * 60)
            await self.kill(view, time_hours, time_min, interaction)
        else:
            await interaction.response.send_message(content="Иди в <#1159910588554678272>, клоун", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_button_click(interaction):
        id = interaction.custom_id
        await interaction.respond(content={id})