from discord.utils import get

def is_connected(voice_client):
    return voice_client and voice_client.is_connected()

def check_ban(interaction, role):
    role = get(interaction.guild.roles, name=role)
    if not role:
        return False
    roles = interaction.user.roles
    return role in roles
