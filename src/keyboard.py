from turtledemo.penrose import start

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True) # основа для кнопок
info = types.KeyboardButton("Информация")
stats = types.KeyboardButton("Статистика")
start.add(stats, info) # добавляем кнопки в основу бота

base = InlineKeyboardMarkup() # основа для инлайн кнопок
base.add(InlineKeyboardButton(f'Да', callback_data='join')) # кнопка и колбэк к ней
base.add(InlineKeyboardButton(f'Нет', callback_data='cancel')) # кнопка и колбэк к ней
