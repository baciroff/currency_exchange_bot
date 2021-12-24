import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<название валюты> \
<в какую валюту перевести> <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    text += "\n".join(f'{i + 1} {key}' for i, key in enumerate(keys.keys()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    values = list(map(str.lower, values))
    try:
        total_base = Converter.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {values[0]} {values[1]} {values[2]} - {total_base}'
        bot.reply_to(message, text)


bot.polling()
