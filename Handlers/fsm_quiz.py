from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import random
import english_dict
from create_bot import bot
from Keyboards import kb_startup

class FSMAdmin(StatesGroup):
    question = State()
    answer_check = State()


async def quiz_start(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Поехали'))
    markup.add(types.KeyboardButton('стоп'))
    await bot.send_message(message.chat.id, 'Добро пожловать в Quiz по редким словам в Английском языке, чтобы начать: нажмите "Поехали", чтобы выйти: нажмите "стоп".', reply_markup=markup)
    async with state.proxy() as data:
        data['counter'] = 0
        data['counter_correct'] = 0
        data['counter_incorrect'] = 0
    await FSMAdmin.question.set()


async def question(message: types.Message, state: FSMContext):
    quiz_list = english_dict.quiz_attempt()
    dictionary = english_dict.eng_dict
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    correct = random.choice(quiz_list)
    await state.update_data(correct=dictionary[correct])
    async with state.proxy() as data:
        data['counter'] += 1
        data[data['counter']] = [correct]
    for i in range(4):
        markup.add(types.KeyboardButton(dictionary[quiz_list[i]]))
    await bot.send_message(message.chat.id, f"'{correct}' is:", reply_markup=markup)
    await FSMAdmin.answer_check.set()


#@dp.message_handler(state=FSMAdmin.question)
async def answer_check(message: types.Message, state: FSMContext):
    answers = await state.get_data()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('стоп'))
    markup.add(types.KeyboardButton('Следующий вопрос'))
    if message.text == answers['correct']:
        await message.reply("Правильно!", reply_markup=markup)
        async with state.proxy() as data:
            data[data['counter']].append("Правильно!")
            data['counter_correct'] += 1
    else:
        await message.reply(f"Неправильно, правильный ответ: {answers['correct']}", reply_markup=markup)
        async with state.proxy() as data:
            data[data['counter']].append(f"Неправильно, правильный ответ: {answers['correct']}")
            data['counter_incorrect'] += 1
    await FSMAdmin.question.set()


#@dp.message_handler(state="*", commands='стоп')
#@dp.message_handler(message='стоп', ignore_case=True, state="*")
async def stop_quiz(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    stats = await state.get_data()
    print(stats)
    await bot.send_message(message.chat.id, f"Количество пройденных вопросов: {stats['counter']}\n Правильных ответов: {stats['counter_correct']}\n Неправильных ответов: {stats['counter_incorrect']}")
    await state.finish()
    await bot.send_message(message.chat.id, 'Quiz завершен!', reply_markup=kb_startup)


def register_handlers_fsmquiz(dp):
    dp.register_message_handler(stop_quiz, text='стоп', state=[FSMAdmin.question, FSMAdmin.answer_check])
    dp.register_message_handler(stop_quiz, commands='стоп', state=[FSMAdmin.question, FSMAdmin.answer_check])
    dp.register_message_handler(quiz_start, commands='QUIZ', state="*")
    dp.register_message_handler(question, state=FSMAdmin.question)
    dp.register_message_handler(answer_check, state=FSMAdmin.answer_check)

