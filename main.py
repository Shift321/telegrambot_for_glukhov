import asyncio
from aiogram import Bot, executor, Dispatcher
from aiogram import types

bot = Bot(token="6959983203:AAHaLEB1U3YJkAXAxXFt2a9eTOmVt7YCRTU")
dp = Dispatcher(bot)

admin_list = [641009347, 714611623]

state = {}


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer(
        'Напишите свое сообщение')


@dp.message_handler(commands="anwser_to_message")
async def anwser_to_message(message: types.Message):
    state[message.chat.id] = {'state': 'anwser_to_message'}
    await message.answer("Введи циферки")


@dp.message_handler()
async def message_handler(message: types.Message):
    if message.chat.id in state.keys():
        if state[message.chat.id]['state'] == 'message_to_anwser':
            anwser_message = f'Тебе пришел ответ:\n\n{message.text}'
            await bot.send_message(state[message.chat.id]['chat_id'], anwser_message)
            state.pop(message.chat.id)
            await message.answer('отправлено')
        if message.chat.id in state.keys():
            if state[message.chat.id]['state'] == 'anwser_to_message':
                state[message.chat.id] = {'chat_id': int(message.text)}
                state[message.chat.id]['state'] = 'message_to_anwser'
                await message.answer('теперь введи сообщение ответа')
    else:
        message_string = f"Тебе пришло новое анонимное сообщение вот его содержание:\n\n{message.text} \n\nчтобы ответить нажми /anwser_to_message и введи циферки {message.chat.id}"
        for i in admin_list:
            await bot.send_message(i, message_string)
        await message.answer('Твое сообщение отправленно')


executor.start_polling(dp)
