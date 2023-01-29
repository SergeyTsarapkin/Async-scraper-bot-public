from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/sobaka')
b2 = KeyboardButton('/koshka')
b3 = KeyboardButton('/Английский')
b4 = KeyboardButton('/Quiz')
b5 = KeyboardButton('/Парсинг_ФТС')

kb_startup = ReplyKeyboardMarkup(resize_keyboard=True)

kb_startup.add(b1).insert(b2).insert(b3).insert(b4).insert(b5)
