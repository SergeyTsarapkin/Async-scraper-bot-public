import Handlers.parsing_dicts
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from Keyboards import kb_startup
from Handlers.FTS_Parser import scrape_in_cycles
from Handlers import Parsing_buttons
from Handlers.parsing_dicts import *
import calendar
import datetime


class FSMAdmin(StatesGroup):
    parameters_setting = State()
    parameters_list = State()
    direction = State()
    period = State()
    custom_period = State()
    countries = State()
    custom_countries = State()
    tnvedlevel = State()
    tnved = State()
    feddistr = State()
    add_distr = State()
    fedsubj = State()
    check_up = State()
    fetching_data = State()


async def start_fetching(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Начать'))
    markup.add(types.KeyboardButton('Загрузить список'))
    markup.add(types.KeyboardButton('Стоп'))
    await bot.send_message(message.chat.id,
                           'Добро пожаловать в скрейпер ФТС, чтобы выбрать параметры в ручную, нажмите "Начать", '
                           'чтобы загрузить параметры списком, нажмите "Загрузить список", чтобы выйти нажмите "Стоп"',
                           reply_markup=markup)
    async with state.proxy() as payload:
        #payload['direction'] = ""
        payload['periodTab'] = "YY"
        #payload['period'] = []
        #payload['countries'] = []
        payload['tnved'] = []
        payload['tnvedLevel'] = 2
        payload['federalDistricts'] = []
        payload['subjects'] = []
        payload['costForm'] = 1
        payload['weightForm'] = 1
    await FSMAdmin.parameters_setting.set()


async def parameters_setting(message: types.Message, state: FSMContext):
    if message.text == 'Загрузить список':
        await bot.send_message(message.chat.id, 'Скопируйте параметры запроса в чат списком в формате: "ДОПИСАТЬ ФОРМАТ"')
        await FSMAdmin.parameters_list.set()
    elif message.text == 'Начать':
        await bot.send_message(message.chat.id, 'Введите направление', reply_markup=Parsing_buttons.kb_direction)
        await FSMAdmin.direction.set()


async def direction(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text == "Импорт":
            payload['direction'] = "ИМ"
        elif message.text == "Экспорт":
            payload['direction'] = "ЭК"
        elif message.text == "Импорт и Экспорт":
            payload['direction'] = ""
        else:
            await message.reply("Выберите направление из меню ниже", reply_markup=Parsing_buttons.kb_direction)
            #await FSMAdmin.direction.set()
    if 'direction' in payload:
        await FSMAdmin.period.set()
        await bot.send_message(message.chat.id, 'Выберите период', reply_markup=Parsing_buttons.period)


async def period(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text == 'Все года':
            payload['periodTab'] = 'AL'
            payload['period'] = []
        elif message.text == '2019':
            payload['period'] = [{"start": "2018-12-31", "end": "2019-12-31"}]
        elif message.text == '2020':
            payload['period'] = [{"start": "2019-12-31", "end": "2020-12-31"}]
        elif message.text == '2021':
            payload['period'] = [{"start": "2020-12-31", "end": "2021-12-31"}]
        elif message.text == '2022':
            payload['period'] = [{"start": "2021-12-31", "end": "2022-12-31"}]
        elif message.text == 'Ввести произвольный период':
            await message.reply('Введите требуемый период в формате "ГГГГ:ММ - ГГГГ:ММ" ')
            await FSMAdmin.custom_period.set()
        else:
            await message.reply('Выберите период из меню ниже', reply_markup=Parsing_buttons.period)
    if 'period' in payload:
        await FSMAdmin.countries.set()
        await bot.send_message(message.chat.id, 'Введите страны', reply_markup=Parsing_buttons.countries)


async def custom_period(message: types.Message, state: FSMContext):
    date = {}
    date_range = message.text.split(' - ')
    print(date_range)
    start_year = int(date_range[0][:4])
    start_month = int(date_range[0][5:7])
    start_day = calendar.monthrange(start_year, start_month)[1]
    start = datetime.date(start_year, start_month, start_day)
    date['start'] = start.strftime('%Y-%m-%d')
    end_year = int(date_range[1][:4])
    end_month = int(date_range[1][5:7])
    end_day = calendar.monthrange(end_year, end_month)[1]
    end = datetime.date(end_year, end_month, end_day)
    date['end'] = end.strftime('%Y-%m-%d')
    async with state.proxy() as payload:
        payload['period'] = [date]
    await bot.send_message(message.chat.id, 'Выберите страны', reply_markup=Parsing_buttons.countries)
    await FSMAdmin.countries.set()


async def countries(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text == "Все страны":
            payload['countries'] = []
        elif message.text == "Страны G20":
            payload['countries'] = g_20
        elif message.text == "Страны G8":
            payload['countries'] = g_8
        elif message.text == "Евросоюз":
            payload['countries'] = european_union
        elif message.text == "Ввести произвольные страны":
            await message.reply('Введите список стран, каждую в новом сообщении')
            await FSMAdmin.custom_countries.set()
        else:
            await message.reply('Выберите опцию из меню ниже') #reply_markup=Parsing_buttons.countries)
    if 'countries' in payload:
        await FSMAdmin.tnvedlevel.set()
        await bot.send_message(message.chat.id, 'Выберите кол-во знаков кода ТНВЭД', reply_markup=Parsing_buttons.tnved_lvl)


async def custom_countries(message: types.Message, state:FSMContext):
    country = message.text
    if country not in ([val for val in countries_list.values()]):
        await message.reply(f'некорректное название страны:"{country}", введите другое')
    else:
        async with state.proxy() as payload:
                payload['countries'].append([key for key, value in countries_list.items() if country in value])
                data = await state.get_data()
                await bot.send_message(message.chat.id, data)


async def tnvedlevel(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        payload['tnvedLevel'] = int(message.text)
    await FSMAdmin.tnved.set()
    await bot.send_message(message.chat.id, 'Нажмите "Все", или введите нужные коды, через запятую', reply_markup=Parsing_buttons.tnved)


async def tnved(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text == 'Пропустить (все коды)':
            payload['tnved'] = []
        else:
            payload['tnved'] = message.text.split(", ")
    await FSMAdmin.feddistr.set()
    await bot.send_message(message.chat.id, 'Выберите федеральные округа', reply_markup=Parsing_buttons.feddistr)



async def feddisrt(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text == 'Все округа':
            payload['federalDistricts'] = []
            data = await state.get_data()
            await bot.send_message(message.chat.id, data)
            await bot.send_message(message.chat.id, 'Проверьте правильность запроса, и нажмите "Выгрузить" или "Исправить запрос"', reply_markup=Parsing_buttons.check_up)
            await FSMAdmin.check_up.set()
        elif message.text in fed_districts_dict:
            key = message.text
            if key not in payload['federalDistricts']:
                payload['federalDistricts'] = [fed_districts_dict[key]]
            else:
                payload['federalDistricts'].append(fed_districts_dict[key])
            await FSMAdmin.add_distr.set()
            await bot.send_message(message.chat.id, 'Выберите дополнительные округа, или нажмите "Завершить выбор"', reply_markup=Parsing_buttons.feddistr)
        elif message.text == 'Завершить выбор':
            data = await state.get_data()
            await bot.send_message(message.chat.id, data)
            #await bot.send_message(message.chat.id, 'Выберите субъект в округе', reply_markup=Parsing_buttons.subj_buttons(payload['federalDistricts']))
            await bot.send_message(message.chat.id, 'Проверьте правильность запроса, и нажмите "Выгрузить" или "Исправить запрос"', reply_markup=Parsing_buttons.check_up)
            await FSMAdmin.check_up.set()
        else:
            await message.reply('Выберите вариант из меню снизу')


async def add_distr(message: types.Message, state: FSMContext):
    async with state.proxy() as payload:
        if message.text in fed_districts_dict:
            payload['federalDistricts'].append(fed_districts_dict[message.text])
        elif message.text == 'Завершить выбор':
            data = await state.get_data()
            await bot.send_message(message.chat.id, data)
            await bot.send_message(message.chat.id, 'Проверьте правильность запроса, и нажмите "Выгрузить" или "Исправить запрос"', reply_markup=Parsing_buttons.check_up)
            await FSMAdmin.check_up.set()
        else:
            await message.reply('Выберите вариант из меню снизу')


async def check_up(message: types.Message, state:FSMContext):
    if message.text == 'Выгрузить':
        payload = await state.get_data()
        id = message.chat.id
        await scrape_in_cycles(payload, id)
        await bot.send_document(message.chat.id, document=open('C:/Users/tsara/PycharmProjects/AIOgram_clean/FTS_data.xlsx', 'rb'))
        await state.finish()
        await bot.send_message(message.chat.id, 'Вышли из парсинга.', reply_markup=kb_startup)

#async def fetching_data(message: types.Message, state: FSMContext):
#    data = await state.get_data()
#    print(data)
#    df = await main(data)
#    print(df)
#    await bot.send_document(message.chat.id, document=open('C:/Users/tsara/PycharmProjects/AIOgram_clean/sample_data.xlsx', 'rb'))


#async def fedsubj(message: types.Message, state: FSMContext):
    #async with state.proxy() as payload:
     #   for district in payload['federalDistricts']:


    #check_up = await state.get_data()
    #await bot.send_message(message.chat.id, check_up)
    #print(check_up)
    #async with state.proxy() as payload:

    #    print(payload)
    #data = await state.get_data()
    #df = await main(data)
    #await bot.send_message(message.chat.id, f'Проверьте данные запроса: {data}')
    #df = await main()
    #await bot.send_document(message.chat.id, document=open('C:/Users/tsara/PycharmProjects/AIOgram_clean/sample_data.xlsx', 'rb'))










async def stop_parsing(message: types.Message, state: FSMContext):
    #current_state = await state.get_state()
    #if current_state is None:
    #    return
    await state.finish()
    await bot.send_message(message.chat.id, 'Вышли из парсинга.', reply_markup=kb_startup)


def register_handlers_fts_parsing(dp):
    dp.register_message_handler(stop_parsing, text='stop', state="*")
    dp.register_message_handler(stop_parsing, commands='stop', state="*")
    dp.register_message_handler(start_fetching, commands='Парсинг_ФТС', state="*")
    dp.register_message_handler(parameters_setting, state=FSMAdmin.parameters_setting)
    dp.register_message_handler(direction, state=FSMAdmin.direction)
    dp.register_message_handler(period, state=FSMAdmin.period)
    dp.register_message_handler(custom_period, state=FSMAdmin.custom_period)
    dp.register_message_handler(countries, state=FSMAdmin.countries)
    dp.register_message_handler(custom_countries, state=FSMAdmin.custom_countries)
    dp.register_message_handler(tnved, state=FSMAdmin.tnved)
    dp.register_message_handler(tnvedlevel, state=FSMAdmin.tnvedlevel)
    dp.register_message_handler(feddisrt, state=FSMAdmin.feddistr)
    dp.register_message_handler(add_distr, state=FSMAdmin.add_distr)
    #dp.register_message_handler(fedsubj, state=FSMAdmin.fedsubj)
    dp.register_message_handler(check_up, state=FSMAdmin.check_up)
    #dp.register_message_handler(fetching_data, state=FSMAdmin.fetching_data)



    #dp.register_message_handler(parameters_loop, state=FSMAdmin.parameters_loop)



































#def fts_scrape():
#    url = "http://stat.customs.gov.ru/api/DataAnalysis/Search"
#    data_to_save = []
#    for x in range(1, 3):
#        querystring = {"page": x, "pageSize": "1"}
#        payload = {
#            "direction": "",
#            "periodTab": "ММ",
#            "period": [{"start": "2022-01-01",
#                        "end": "2022-03-31"}],
#            "countries": ['US'],
#            "tnved": [],
#            "tnvedLevel": 2,
#            "federalDistricts": [],
#            "subjects": [],
#            "costForm": 1,
#            "weightForm": 1
#        }
#        headers = {
#            "Accept": "application/json, text/plain, */*",
#            "Accept-Language": "ru-RU",
#            "Connection": "keep-alive",
#            "Content-Type": "application/json",
#            "Origin": "http://stat.customs.gov.ru",
#            "Pragma": "no-cache",
#            "Referer": "http://stat.customs.gov.ru/analysis",
#            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
#        }
#        r = requests.request("POST", url, json=payload, headers=headers, params=querystring)
#
#        data = r.json()
#        for _ in data['data']:
#            data_to_save.append(_)
#    #df = pd.DataFrame.from_dict((r.json()['data']))
#
#    df = pd.json_normalize(data_to_save)
#    return(df)