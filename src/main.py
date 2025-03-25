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
