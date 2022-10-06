import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Comandos:
!help - muestra la lista de comandos
!p <keywords> - Busca la canción solicitada en youtube y la agrega a la cola. En caso de no haber cola, reproduce
!q - muestra las canciones que están en cola
!skip - saltea la siguiente canción
!clear - detiene la canción actual y limpia la lista de reproducción
!leave - desconecta al bot del voice channel
!pause - pausa la canción actual
!resume - reanuda la canción actual
```
"""
        self.text_channel_list = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        await self.send_to_all(self.help_message)        

    @commands.command(name="help", help="Muestra los comandos disponibles")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)