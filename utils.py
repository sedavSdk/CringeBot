from discord.utils import get


def is_connected(interaction, channel):
    return channel and interaction.guild.voice_client

def check_ban(interaction, role):
    role = get(interaction.guild.roles, name=role)
    if not role:
        return False
    roles = interaction.user.roles
    return role in roles

async def log(interaction, message, channel):
    channel = get(interaction.guild.channels, id=channel)
    if channel:
        await channel.send(message)