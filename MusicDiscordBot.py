import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv()

API_KEY_DISCORD = "INSERTE SU API KEY"

#importar cogs
from help_cog import help_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Remover el comando 'help' que viene por defecto
bot.remove_command('help')

#Añadir cogs al bot

async def add():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))   

asyncio.run(add())

#Iniciar bot con token

bot.run(API_KEY_DISCORD)