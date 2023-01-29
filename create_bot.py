import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

admin_id = os.getenv('admin_id')
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(bot, storage=storage)