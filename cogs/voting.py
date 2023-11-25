from discord.ext import commands
import discord
import datetime
from discord import app_commands
import asyncio
import configparser
from random import choice
import time
import sys
sys.path.append("..")
from utils import clamp

#da

class CogVoiting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.id : int = 1

        self.config = configparser.ConfigParser()
        self.config.read('cogs.ini')
        self.voteChannel = self.config.getint('id', 'vote_chennel_id')


    class Ful(discord.ui.View):
        def __init__(self, theme, id, config, guild, time, args=[]):
            super().__init__()
            self.args = args
            self.id = id
            self.nowId = 1
            self.heading = theme
            self.content = [""] * 7
            self.vouts = [0] * 7
            self.circles = ["🟢", "🟠", "🟣", "🟤", "🟡", "🔵", "🔴"]
            self.users = {}
            self.colour = discord.Colour.from_rgb(173, 255, 47)
            self.boardOfShameId = config.getint('id', 'board_of_shame_id')
            self.boardOfShame = discord.utils.get(guild.channels, id=self.boardOfShameId)
            self.message_time = datetime.datetime.now()
            self.time = time
            self.timeout = None

            for i in range(0, len(args)):
                if len(args[i]) > 0:
                    self.content[i] = self.args[i]
                    b = self.Btn(label= self.circles[i] + ' ' + args[i], custom_id=f"{self.id}.{self.nowId}", ful=self, number=i)
                    self.add_item(b)
                    self.nowId += 1
            self.add_item(self.BtnRevote(custom_id=f"{self.id}.{self.nowId}", ful=self))
            
        def getContent(self, timer=False):
            str = "" 
            for i in range(0, len(self.content)):
                if len(self.content[i]) > 0:
                    str += "\n" + "`" + self.circles[i] + f' {self.vouts[i]}` - ' + self.content[i]
            if timer:
                str += "\n\nГолосование завершится " + f'<t:{int(time.mktime(self.message_time.timetuple()) + self.time)}:R>'
            c2 = discord.Embed(color=self.colour, description=str, title=self.heading + "\n")
            return c2
        
        
        class Btn(discord.ui.Button):
            def __init__(self, label, custom_id, ful, number):
                super().__init__(label=label, custom_id=custom_id)
                self.callback = self.button_callback
                self.voteNumber = 0
                self.ful = ful
                self.number = number
                self.channel = None

            
            async def button_callback(self, interaction):
                    if interaction.user.id not in self.ful.users:
                        self.ful.vouts[self.number] += 1
                        self.ful.users[interaction.user.id] = 1
                    await interaction.response.edit_message(embed=self.ful.getContent(timer=True))
        
        class BtnRevote(discord.ui.Button):
            def __init__(self, custom_id, ful):
                super().__init__(label="🔄 Переголосовать", custom_id=str(custom_id) + "revote")
                self.ful = ful
                self.callback = self.button_callback
                self.style = discord.ButtonStyle.blurple
            
            async def button_callback(self, interaction):
                if interaction.user.id not in self.ful.users:
                    await interaction.response.send_message(content=f"Проголосуй сначала", ephemeral=True)
                else:
                    role = discord.utils.get(interaction.guild.roles, name="Переголосовавший")
                    if role not in interaction.user.roles:
                        await interaction.user.add_roles(role)
                        m = ["может вообще не будешь голосовать?", "может ну его нахуй вообще?", "может съебёшься с канала?"]
                        await self.ful.boardOfShame.send(f"{interaction.user.mention} если ты с первого раза не можешь нормально проголосовать, {choice(m)}")
                    await interaction.response.send_message(content=f"Ищи себя на доске позора {self.ful.boardOfShame.mention}", ephemeral=True)
        
    async def kill(self, thing_for_del, time, interaction: discord.Interaction):
        print(f"{datetime.datetime.now()}: start timer, vote created by {interaction.user}, expired in {time / 60} seconds, id = {thing_for_del.id} ")
        await asyncio.sleep(time)
        await thing_for_del.channel.send(embed=thing_for_del.getContent(), content="✅ Голосование завершено")
        print(f"{datetime.datetime.now()}: vote created by {interaction.user} with id = {thing_for_del.id}  ended")
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
    async def createVote(self, interaction: discord.Interaction, theme : str, variant1 : str, variant2: str, time_hours : int = 0, time_min : int = 10, variant3: str="", variant4: str="", variant5: str="", variant6: str="", variant7: str=""):
        if interaction.channel_id == self.voteChannel:
            time_hours = clamp(time_hours, 0, 24)
            time_min = clamp(time_min, 1, 59)
            args = [variant1, variant2, variant3, variant4, variant5, variant6, variant7]
            time = time_hours * 3600 + time_min * 60
            view = self.Ful(theme, self.id, self.config, interaction.guild, time, args)
            self.id = view.id
            view.channel = interaction.channel
            await interaction.response.send_message(embed=view.getContent(timer=True), view=view, delete_after=time)
            await self.kill(view, time, interaction)
        else:
            await interaction.response.send_message(content="Иди в <#1159910588554678272>, клоун", ephemeral=True)