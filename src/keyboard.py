from turtledemo.penrose import start

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True) # основа для кнопок

info = types.KeyboardButton("Информация")
stats = types.KeyboardButton("Статистика")
razrab = types.KeyboardButton("Разработчик")
user = types.KeyboardButton("Покажи пользователя")
photo = types.KeyboardButton("Отправить фото")

start.add(stats, info, razrab, user, photo) # добавляем кнопки в основу бота

base = InlineKeyboardMarkup() # основа для инлайн кнопок
base.add(InlineKeyboardButton(f'Да', callback_data='join')) # кнопка и колбэк к ней
base.add(InlineKeyboardButton(f'Нет', callback_data='cancel')) # кнопка и колбэк к ней

usr = InlineKeyboardMarkup() # основа для инлайн кнопок
usr.add(InlineKeyboardButton(f'хочу увидеть id', callback_data='id')) # кнопка и колбэк к ней
usr.add(InlineKeyboardButton(f'вернуться обратно', callback_data='back')) # кнопка и колбэк к ней