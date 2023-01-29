import pandas as pd
import time
import asyncio
from aiohttp import ClientSession
from aiolimiter import AsyncLimiter
from create_bot import bot


headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://stat.customs.gov.ru",
        "Pragma": "no-cache",
        "Referer": "http://stat.customs.gov.ru/analysis",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }


async def fetch(id, msg_resp_id, url, session, payload, querystring, result):
    async with session.post(url, json=payload, headers=headers, params=querystring, ssl=False) as resp:
        data = await resp.json()
        if 'data' in data:
            print(f"received a response {data['currentPage']}")
            if data['currentPage'] % 10 == 0:
                await bot.edit_message_text(f"Получено ответов: {data['currentPage']}.", id, msg_resp_id)
            for row in data['data']:
                result.append(row)
        return result


async def fetch_with_throttle(id, msg_req_id, msg_resp_id, url, session, payload, querystring, page, throttler, limit, result):
    async with limit, throttler:
        print(f'sending a request {page}')
        if page % 10 == 0:
            await bot.edit_message_text(f"Отправлено запросов: {page}", id, msg_req_id)
        return await fetch(id, msg_resp_id, url, session, payload, querystring, result)


async def get_pages(url, json, session, querystring):
    async with session.post(url, json=json, headers=headers, params=querystring) as resp:
        pages_count = await resp.json()
        print(f'Всего страниц к скачиванию: {pages_count["pageCount"]}')
        return pages_count['pageCount']


async def scrape_in_cycles(payload, id):
    url = "http://stat.customs.gov.ru/api/DataAnalysis/Search"
    limit = asyncio.Semaphore(5)
    tasks = []
    result = []
    throttler = AsyncLimiter(max_rate=5, time_period=1)
    async with ClientSession() as session:
        pages = await get_pages(url, json=payload, session=session, querystring={'page': '1', 'pageSize': '300'})
        await bot.send_message(id, f'Начинаю парсинг, кол-во запросов которое будет отправлено на сервер ФТС: {pages}.')
        msg_requests = await bot.send_message(id, "Отправлено запросов: 0")
        msg_req_id = msg_requests.message_id
        msg_response = await bot.send_message(id, "Получено ответов: 0")
        msg_resp_id = msg_response.message_id
        cycles = pages // 100
        remainder = pages % 100
        lower_page, upper_page = 1, 100
    for cycle in range(cycles):
        async with ClientSession() as session:
            for page in range(lower_page, upper_page+1):
                querystring = {"page": page, "pageSize": "300"}
                tasks.append(asyncio.create_task(fetch_with_throttle(id, msg_req_id, msg_resp_id, url, session, payload, querystring, page, throttler, limit, result)))
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
        lower_page += 100
        upper_page += 100
    if cycles == 0:
        upper_page = 1
    print(remainder)
    if remainder > 0:
        print('getting the remaining pages')
        async with ClientSession() as session:
            for page in range(upper_page+1, pages+1):
                querystring = {"page": page, "pageSize": "300"}
                tasks.append(asyncio.create_task(fetch_with_throttle(id, msg_req_id, msg_resp_id, url, session, payload, querystring, page, throttler, limit, result)))
            await asyncio.gather(*tasks)
    df = pd.DataFrame(result)
    df['period'] = pd.to_datetime(df['period']).dt.date
    df = df.sort_values(by='period')
    await bot.send_message(id, 'Начало создания excel таблицы')
    df.to_excel('FTS_data.xlsx', sheet_name='sheet1', index=False)
    await bot.send_message(id, 'Excel таблица создана, ожидается отправка.')


#async def main(payload, id):
#    tasks = []
#    result = []
#    url = "http://stat.customs.gov.ru/api/DataAnalysis/Search"
#    throttler = AsyncLimiter(max_rate=5, time_period=1)
#    async with ClientSession() as session:
#        pages = await get_pages(url, json=payload, session=session, querystring={'page': '1', 'pageSize': '300'})
#        await bot.send_message(id, f'Начинаю парсинг, кол-во запросов которое будет отправлено на сервер ФТС: {pages}.')
#        msg_requests = await bot.send_message(id, "Отправлено запросов: 0")
#        msg_req_id = msg_requests.message_id
#        msg_response = await bot.send_message(id, "Получено ответов: 0")
#        msg_resp_id = msg_response.message_id
#        for page in range(1, pages+1):
#            querystring = {"page": page, "pageSize": "300"}
#            tasks.append(asyncio.create_task(fetch_with_throttle(id, msg_req_id, msg_resp_id, url, session, payload, querystring, page, throttler, result)))
#        await asyncio.gather(*tasks)
#    df = pd.DataFrame(result)
#    df['period'] = pd.to_datetime(df['period']).dt.date
#    df = df.sort_values(by='period')
#    await bot.send_message(id, 'Начало создания excel таблицы')
#    df.to_excel('FTS_data.xlsx', sheet_name='sheet1', index=False)
#    await bot.send_message(id, 'Excel таблица создана, ожидается отправка.')

#p = {
#        "direction": "ИМ",
#        "periodTab": "",
#        "period": [],
#        "countries": ['JP'],
#        "tnved": [],
#        "tnvedLevel": 2,
#        "federalDistricts": [],
#        "subjects": [],
#        "costForm": 1,
#        "weightForm": 1
#    }
