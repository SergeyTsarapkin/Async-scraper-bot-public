from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Английский')
b2 = KeyboardButton('/Quiz')
b3 = KeyboardButton('/Парсинг_ФТС')

kb_startup = ReplyKeyboardMarkup(resize_keyboard=True)

kb_startup.add(b1).insert(b2).insert(b3)
