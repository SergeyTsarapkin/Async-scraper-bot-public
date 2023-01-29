from aiogram import types
import Keyboards
import english_dict
from create_bot import bot
#from Handlers import urls

async def command_start(message : types.message):
    await bot.send_message(message.chat.id, "Приветствую", reply_markup=Keyboards.kb_startup)
    await bot.send_message(message.chat.id, message.chat.id)

async def random_english_word(message : types.message):
    answer = english_dict.random_word()
    first_word = answer.split()[0]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(first_word, url=f"https://en.wikipedia.org/wiki/{first_word}"))
    await bot.send_message(message.chat.id, answer, reply_markup=markup)

#async def echo(message : types.message):
#    await message.reply(message.text)

def register_handlers_general(dp):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    #dp.register_message_handler(random_animal_picture, commands=['sobaka', 'koshka'])
    dp.register_message_handler(random_english_word, commands=['Английский'])
    #dp.register_message_handler(echo)