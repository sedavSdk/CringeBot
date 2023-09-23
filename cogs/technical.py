from discord.ext import commands
from discord import utils
import sys
import json
sys.path.append("..")
from utils import is_connected

class CogTech(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.WHITELIST = 0
        self.BLACKLIST = 1

        self.roles = [[], []]
        self.roles_status = self.WHITELIST
        self.users = [[], []]
        self.users_status = self.WHITELIST
        self.channels = [[], []]
        self.channels_status = self.BLACKLIST

        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
                roles = self.data['roles']
                roles_status = self.data['roles_status']
                users = self.data['users']
                channels = self.data['channels']
                print("data load completed")
        except:
            print("data load failed")
            pass
    
    @commands.has_role('botMaster')
    @commands.command(description='Выключить (скорее всего вы это юзать не можете)')
    async def stop(self, ctx):
        voice_client = utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if is_connected(voice_client):
            await voice_client.disconnect()
        with open('data.json', 'w') as f:
            data = {
                'users': self.users,
                'users_status': self.users_status,
                'roles': self.roles,
                'roles_status': self.roles_status,
                'channels': self.channels,
                'channels_status': self.channels_status
            }
            json.dump(data, f)
            
        sys.exit()
    
    def check_role(self, ctx):
        user = ctx.author
        if user.guild_permissions.administrator:
            return True
        if self.roles_status == self.WHITELIST:
            for role in user.roles:
                if role in self.roles[self.WHITELIST]:
                    return True
            return False
        else:
            for role in user.roles:
                if role in self.roles[self.BLACKLIST]:
                    return False
            return True
        
    def check_user(self, ctx):
        user = ctx.author
        if user.guild_permissions.administrator:
            return True
        if self.users_status == self.WHITELIST:
            return user in self.users[self.WHITELIST]
        else:
            return user not in self.users[self.BLACKLIST]
            
    def check_channel(self, ctx):
        channel = ctx.channel
        if self.channels_status == self.WHITELIST:
            return channel in self.channels[self.WHITELIST]
        else:
            return channel not in self.channels[self.BLACKLIST]
    
    @commands.command()
    async def access(self, ctx, accessList, typeList, data):
        if accessList.lower() in ["users", "roles", "channels"]:
            edit = [self.users, self.roles, self.channels][["users", "roles", "channels"].index(accessList.lower())]
            if typeList.lower() in ["whitelist", "blacklist"]:
                wl = [self.WHITELIST, self.BLACKLIST][["whitelist", "blacklist"].index(typeList.lower())]
                edit[wl].append(data)
            else:
                ctx.send("Неправильный тип, используйте whitelist или blacklist")
        else:
            ctx.send("Неправильный список, используйте users, roles или channels")

    @commands.command()
    async def changeAccess(self, ctx, accessList):
        if accessList.lower() in ["users", "roles", "channels"]:
            accessList = accessList.lower()
            message = str(ctx.author) + ' изменил тип {} с '.format(accessList)
            if accessList == "users":
                message += ['whitelist', 'blacklist'][self.users_status]
                self.users_status = (self.users_status + 1) % 2
                message += ' на ' + ['whitelist', 'blacklist'][self.users_status]
            elif accessList == "roles":
                message += ['whitelist', 'blacklist'][self.roles_status]
                self.roles_status = (self.roles_status + 1) % 2
                message += ' на ' + ['whitelist', 'blacklist'][self.roles_status]
            elif accessList == "channels":
                message += ['whitelist', 'blacklist'][self.channels_status]
                self.channels_status = (self.channels_status + 1) % 2
                message += ' на ' + ['whitelist', 'blacklist'][self.channels_status]
            await self.log(ctx, message)
        else:
            ctx.send("Неправильный список, используйте users, roles или channels")