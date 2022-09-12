import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import expenses
import Exceptions
import aiohttp
from categories import Categories


API_TOKEN = '5477041709:AAFksJ7Uga3TZX5pFSp757ntKjkA9Lp9QnA'
ACCESS_ID = 598856945

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, loop=loop)
#dp.middleware.setup(AccessMiddleware(ACCESS_ID))

# def auth(func):
# #
#      async def wrapper(message):
#          if message['from']['id'] != 598856945:
#              return await message.reply('Acces denied', reply = False)
#          return await func(message)
#      return wrapper
#
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories \n"
        "Полная Статистика: /all_stats")

@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)

@dp.message_handler(commands=['month'])
async def month_statistic(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)

@dp.message_handler(commands=['all_stats'])
async def all_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_all_statistics_per_month()
    await message.answer(answer_message)

@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text)
    except Exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = "Добавлены траты на %s руб по категории: %s ." % (str(expense.amount), str(expense.category_name))
  #      f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)
async def send_to_admin(*args):
    await bot.send_message(chat_id=ACCESS_ID, text="Бот запущен")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=send_to_admin)
