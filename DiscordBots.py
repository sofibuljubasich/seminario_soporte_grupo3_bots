import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
API_KEY= "INSERTE SU API KEY"
client = discord.Client(intents=discord.Intents.all())

frases = [
  "Alégrate, un camino de hermosas pasiones te espera y   debes transitarlo",
  "Nunca tendrás que preocuparte por un ingreso estable.",
  "Hoy tendrás un día de increíble alegría y brillara tu     sentido del humor.",
  "Hoy compartirás las horas mas tiernas de tu vida con alguien muy amado.",
  "La rueda de la fortuna te favorecerá y estarás rodeado de prosperidad.",
  "Tendrás entera satisfacción al final de esta temporada. Prepárate.",
  "Muchos se alegraran por tus logros y a ti te mejorara la vida",
  "Eres una persona a la que le gusta triunfar en la vida.",
  "Confía en tu buen juicio y veras que este te lleva al triunfo.",
  "Se te cumplirá un hermoso sueño y veras como otros sueños se hacen realidad.",
  "No olvides que un amigo es un regalo que te das a ti mismo.",
  "Sabes que es exactamente lo que quieres. Trabaja en ello y hazlo materializarse.",
  "Siente la felicidad que espera por ti y no olvides atraparla para mantenerla contigo."
]


@client.event
async def on_ready():
  print('En funcionamiento {0.user}'.format(client))


@client.event
async def on_message(message):
  username = str(message.author).split('#')[0]
  user_message = str(message.content)
  channel = str(message.channel.name)

  print(f'{username}: {user_message} ({channel})')

  if message.author == client.user:
    return

  if message.channel.name == 'bot-testing':
    if user_message.lower() == 'hola':
      await message.channel.send(f'Hola {username},En qué puedo ayudarte?')
      return
    elif user_message.lower() == 'chau':
      await message.channel.send(f'Nos vemos {username}, suerte!')
      return
    elif user_message.lower() == '!phrase':
      i = random.randint(0, 12)
      response = f' {frases[i]} '
      await message.channel.send(response)
      return
    elif user_message.lower() == '!random':
      a = random.randint(0, 10)
      response = f'Tu número de la suerte es {a}'
      await message.channel.send(response)
      return



client.run(API_KEY)
