from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.dispatcher import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import keyboard
import logging

storage = MemoryStorage() # FSM
bot = Bot(token=config.bot_key, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage) # хранилище состояний в оперативной памяти

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, )


class meinfo(StatesGroup):
    Q1 = State()
    Q2 = State()

@dp.message_handler(Command("me"), state=None) # команда /me для админа
async def enter_meinfo(message: types.Message):
    if message.chat.id == config.admin:
        await message.answer("начинаем настройку.\n"
                             "№1 Введите линк на ваш профиль") # бот спрашивает ссылку
        await meinfo.Q1.set()

@dp.message_handler(state=meinfo.Q1) # как только бот получит ответ на /me
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer) # записывает ответ (линк)
    await message.answer("Линк сохранён. \n"
                         "№2 Введите текст.")
    await meinfo.Q2.set()

@dp.message_handler(state=meinfo.Q2) # после того как пришел текст №2
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer) # записывает второй ответ
    await message.answer("Текст сохранён.")

    data = await state.get_data()
    answer1 = data.get("answer1") # запись ответа в переменную, чтобы сохранить в файл и вывести в след. смс
    answer2 = data.get("answer2")

    joinedFile = open("link.txt", "w", encoding="utf-8") # utf-8 для того, чтобы записывались смайлики
    joinedFile.write(str(answer1))
    joinedFile = open("text.txt", "w", encoding="utf-8")
    joinedFile.write(str(answer2))

    await message.answer(f'Ваша ссылка на профиль: {answer1}\nВаш текст:\n{answer2}') # вывод линка с текстом
    await state.finish()


@dp.message_handler(Command("start"), state=None) # задаем название команды start
async def welcome(message):
    joinedFile = open("user.txt", "r") # создаем файл, в который будем записывать id пользователя
    joinedUsers = set()
    for line in joinedFile: # цикл, в котором проверяем имеется ли такой id в файле user
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers: # делаем запись в файл user нового id
        joinedFile = open("user.txt", "a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ",
                           reply_markup=keyboard.start, parse_mode='Markdown')
    # после проверки и записи выводим сообщение с именем пользователя и отображаем кнопки


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Вот статистика бота: *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'У тебя нет админки', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancel')
async def cancel(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ты вернулся в главное меню. Жми кнопки', parse_mode='Markdown')


@dp.message_handler(commands=['rassilka'])
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'*Рассылка началась '
                               f'\nБот оповестит, когда рассылку закончит*', parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open('user.txt', 'r')
        joinedUsers = set()
        for line in joinedFile:
            joinedUsers.add(line.strip())
        joinedFile.close()

        for user in joinedUsers:
            try:
                await bot.send_photo(user, open('una.jpg', 'rb'), message.text[message.text.find(' '):])
                receive_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, f'*Рассылка была завершена *\n'
                               f'получили сообщение: *{receive_users}*\n'
                               f'заблокировали бота: *{block_users}*', parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.text == 'Информация':
        await bot.send_message(message.chat.id, text = 'Информация\nБот создан специально для обучения', parse_mode='Markdown')

    if message.text == 'Статистика':
        await bot.send_message(message.chat.id, text='Хочешь посмотреть статистику бота?', reply_markup=keyboard.base, parse_mode='Markdown')

if __name__ == '__main__':
    print('Бот запущен!') # чтобы бот работал всегда с выводом в начале вашего любого текста
executor.start_polling(dp)