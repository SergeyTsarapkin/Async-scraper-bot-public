from create_bot import dp, bot, admin_id
from aiogram.utils import executor
from Keyboards import kb_startup

async def on_startup(_):
    print('Бот вышел в онлайн')
    await bot.send_message(admin_id, "Bot launched!", reply_markup=kb_startup)

async def on_shutdown(_):
    print('Бот закончил работу')
    await bot.send_message(admin_id, "Bot stopped!")

@dp.message_handler(commands="test")
async def language_stuff(message):
    await bot.send_message(message.chat.id, "eh")


import Handlers

Handlers.register_handlers_fsmquiz(dp)
Handlers.register_handlers_general(dp)
Handlers.register_handlers_fts_parsing(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
