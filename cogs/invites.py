from discord.ext import commands
import sys
sys.path.append("..")
from discord import app_commands
import discord
import configparser

class CogInvites(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.invites = []
        self.guild = None
        self.groups = {
            "B3uxrkS9RE": "General",
            "hBt2dYUJjf": "Shooter",
            "N3xEECQtyU": "ARPG",
            "hUNDCqXmnp": "ARPG",
            "Q8EYP5bKDk": "Coop",
            "DYxeBWswjD": "Coop",
            "MkZ8Mfkc2R": "Coop",
            "mbWFuhCkKR": "General",
            "F5APNd6eE3": "Shooter"
        }
        self.names = {
            "B3uxrkS9RE": "ㆍ`⬛ Общее     `ㆍ⬛ **Основная ссылка**",
            "hBt2dYUJjf": "ㆍ`❌ Шутеры    `ㆍ<:1finals:1187158991395094538> **The Finals**",
            "N3xEECQtyU": "ㆍ`🔶 АРПГ      `ㆍ<:2poe:1177685688196542555> **Path of Exile**",
            "hUNDCqXmnp": "ㆍ`🔶 АРПГ      `ㆍ<:2lastepoch:1192469031626743858> **Last Epoch**",
            "Q8EYP5bKDk": "ㆍ`⚪ Кооп      `ㆍ<:3TheFirstDescendant:1262552034880520342> **The First Descendant**",
            "DYxeBWswjD": "ㆍ`⚪ Кооп      `ㆍ⚪ **Основная для Кооп**",
            "MkZ8Mfkc2R": "ㆍ`⚪ Кооп      `ㆍ<:3Dungeonborne:1264608723763204198> **DungeonBorne**",
            "mbWFuhCkKR": "ㆍ`⬛ Общее     `ㆍ⬛ **Для продвижения**",
            "F5APNd6eE3": "ㆍ`❌ Шутеры    `ㆍ<:1hunt:1187160041871130646> **Hunt: Showdown**"
        }
        self.out = {}
    
    async def create_info(self):
        self.invites = await self.guild.invites()
        for i in self.invites:
            if i.code in self.groups:
                formatted_i = f"`{i.uses:4}`"
                if self.groups[i.code] in self.out:
                    self.out[self.groups[i.code]] += ("\n" + formatted_i + self.names[i.code])
                else:
                    self.out[self.groups[i.code]] = formatted_i + self.names[i.code]

    @commands.Cog.listener()
    async def on_ready(self): 
        self.guild = self.client.guilds[0]

    @app_commands.command(name="invites", description='статистика по приглашениям')
    async def show(self, interaction: discord.Interaction):
        if "botMaster" in [role.name for role in interaction.user.roles]:
            await self.create_info()
            str1 = ""
            str1 += self.out["General"] + "\n"
            str1 += self.out["Coop"] + "\n"
            str1 += self.out["Shooter"] + "\n"
            str1 += self.out["ARPG"] + "\n"
            self.out = {}
            await interaction.response.send_message(content=str1)
        else:
            await interaction.response.send_message(content="Права не имеешь!!!", ephemeral=True)
        