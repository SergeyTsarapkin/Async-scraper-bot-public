from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Handlers.parsing_dicts import *
#from Handlers import FTS_Scrape
#import Handlers.FTS_Scrape

direction_im = KeyboardButton('Импорт')
direction_ex = KeyboardButton('Экспорт')
direction_both = KeyboardButton('Импорт и Экспорт')

kb_direction = ReplyKeyboardMarkup(resize_keyboard=True)
kb_direction.add(direction_im, direction_ex, direction_both)

########################################################################################################################

period_all = KeyboardButton('Все года')
period_2019 = KeyboardButton('2019')
period_2020 = KeyboardButton('2020')
period_2021 = KeyboardButton('2021')
period_2022 = KeyboardButton('2022')
period_custom = KeyboardButton('Ввести произвольный период')

period = ReplyKeyboardMarkup(resize_keyboard=True)
period.row(period_all, period_custom).row(period_2019, period_2020, period_2021, period_2022)

########################################################################################################################

countries_all = KeyboardButton('Все страны')
countries_g20 = KeyboardButton('Страны G20')
countries_g8 = KeyboardButton('Страны G8')
countries_eu = KeyboardButton('Евросоюз')
countries_custom = KeyboardButton('Ввести произвольные страны')

countries = ReplyKeyboardMarkup(resize_keyboard=True)
countries.row(countries_custom, countries_all).row(countries_g8, countries_eu, countries_g20)

########################################################################################################################

tnved_02 = KeyboardButton('02')
tnved_04 = KeyboardButton('04')
tnved_06 = KeyboardButton('06')
tnved_08 = KeyboardButton('08')
tnved_10 = KeyboardButton('10')

tnved_lvl = ReplyKeyboardMarkup(resize_keyboard=True)
tnved_lvl.add(tnved_02, tnved_04, tnved_06, tnved_08, tnved_10)

########################################################################################################################

tnved_all = KeyboardButton('Пропустить (все коды)')
tnved_custom = KeyboardButton('Ввести нужные коды')

tnved = ReplyKeyboardMarkup(resize_keyboard=True)
tnved.row(tnved_all, tnved_custom)

########################################################################################################################

feddistr_all = KeyboardButton('Все округа')
feddistr_01 = KeyboardButton('ЦФО')
feddistr_02 = KeyboardButton('СЗФО')
feddistr_03 = KeyboardButton('ЮФО')
feddistr_04 = KeyboardButton('ПФО')
feddistr_05 = KeyboardButton('УФО')
feddistr_06 = KeyboardButton('СФО')
feddistr_07 = KeyboardButton('ДФО')
feddistr_08 = KeyboardButton('СКФО')
feddistr_na = KeyboardButton('Неизвестный ФО')
feddistr_done = KeyboardButton('Завершить выбор')

feddistr = ReplyKeyboardMarkup(resize_keyboard=True)
feddistr.add(feddistr_all, feddistr_01, feddistr_02, feddistr_03, feddistr_04, feddistr_05, feddistr_06, feddistr_06, feddistr_07, feddistr_08, feddistr_na, feddistr_done)

########################################################################################################################


def subj_buttons(chosen_districts):
    fedsubj = ReplyKeyboardMarkup(resize_keyboard=True)
    fedsubj_all = KeyboardButton('Все субъекты')
    fedsubj_confirm = KeyboardButton('Подтвердить')
    fedsubj.add(fedsubj_all, fedsubj_confirm)
    needed_subjects = {}
    for distr in chosen_districts:
        needed_subjects[distr] = fed_subj_dict[distr]
    for subj in fed_subj_dict[district]:
        fedsubj.add(KeyboardButton(subj))
    return fedsubj

########################################################################################################################

check_up_confirm = KeyboardButton('Выгрузить')
check_up_amend = KeyboardButton('Исправить запрос')

check_up = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
check_up.add(check_up_confirm, check_up_amend)



