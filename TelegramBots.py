import os
import telebot
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from telebot import types

load_dotenv()
pd.options.display.float_format = '{:,.2f}'.format
API_KEY = "INSERTE API KEY"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    mensaje = 'Hola En qué puedo ayudarte? Comandos:' + '\n'
    mensaje += '/price nombreAcción --> Precio de una acción últimos 10 días' + '\n'
    mensaje += '/info nombreAcción-->' + '\n'
    mensaje += '/listar --> Devuelve nombre de las acciones mas populares' + '\n'
    mensaje += '/holders nombreAcción-->Info de Holders' + '\n'
    mensaje += '/reco nombreAcción --> Recomendaciones sobre si vender o comprar' + '\n'
    mensaje += 'Para más información de las acciones: finance.yahoo.com/trending-tickers'
    bot.send_message(message.chat.id, mensaje)


@bot.message_handler(commands=['price'])
def send_price(message):
    msg = message.text.split()
    if (len(msg) > 1):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10d', interval='1d')
        if data.size > 0:
            mensaje = "Precios de la acción {a} en los últimos 10 días".format(
                a=request)
            bot.send_message(message.chat.id, mensaje)
            bot.send_message(message.chat.id,
                             data['Close'].to_string(header=False))
        else:
            bot.send_message(message.chat.id, "No data!")
    else:
        bot.send_message(message.chat.id,
                         "Por favor, ingrese un símbolo --> /price tsla")


@bot.message_handler(commands=['holders'])
def send_holders(message):
    msg = message.text.split()
    if (len(msg) > 1):
        request = message.text.split()[1]
        data = yf.Ticker(request)
        if (type(data.institutional_holders) != type(None)):
            mensaje = "Holders de la acción {a}".format(a=request)
            bot.send_message(message.chat.id, mensaje)
            bot.send_message(
                message.chat.id,
                data.institutional_holders[['Holder',
                                            'Shares']].to_string(header=True,
                                                                 index=False))
        else:
            bot.send_message(message.chat.id, "No data!")
    else:
        bot.send_message(message.chat.id,
                         "Por favor, ingrese un símbolo --> /holders tsla")


@bot.message_handler(commands=['info'])
def send_info(message):
    msg = message.text.split()
    if (len(msg) > 1):
        request = message.text.split()[1]
        data = yf.download(tickers=request, period='10d', interval='1d')
        if data.size > 0:
            bot.send_message(
                message.chat.id,
                data[['Open', 'High', 'Low', 'Close',
                      'Volume']].to_string(header=True))
        else:
            bot.send_message(message.chat.id, "No data!")
    else:
        bot.send_message(message.chat.id,
                         "Por favor, ingrese un símbolo --> /info tsla")


@bot.message_handler(commands=['reco'])
def send_recommendation(message):
    msg = message.text.split()
    if (len(msg) > 1):
        request = message.text.split()[1]
        ticker = yf.Ticker(request)
        if (type(ticker.recommendations) != type(None)):
            data = ticker.recommendations
            data = data.iloc[:,
                             1:3].reset_index().head()  #Elimina columna fecha
            mensaje = "Recomendaciones de la acción {a}".format(a=request)
            bot.send_message(message.chat.id, mensaje)
            bot.send_message(message.chat.id,
                             data.to_string(header=True, index=False))
        else:
            bot.send_message(message.chat.id, "No data!")

    else:
        bot.send_message(message.chat.id,
                         "Por favor, ingrese un símbolo --> /info tsla")


@bot.message_handler(commands=['listar'])
def send_lista(message):
    msj = 'Algunas acciones son:' + '\n'
    msj += 'YPF (YPF Sociedad Anónima)' + '\n'
    msj += 'TWTR (Twitter, Inc)' + '\n'
    msj += 'AMZN (Amazon.com, Inc.)' + '\n'
    msj += 'ABNB (Airbnb, Inc.)' + '\n'
    msj += 'TSLA (Tesla, Inc.)' + '\n'
    msj += 'AAPL (Apple Inc.)'
    bot.send_message(message.chat.id, msj)

@bot.message_handler(commands=['opciones'])
def send_opciones(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('/start')
    itembtn2 = types.KeyboardButton('/price AMZN')
    itembtn3 = types.KeyboardButton('/price TWTR')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Seleccione:", reply_markup=markup)


bot.polling()
