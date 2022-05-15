#!venv/bin/python
import logging
from pprint import pprint
import requests
from bs4 import BeautifulSoup

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import Text


# ________________________________________________________________
REQUEST_API_URL = 'http://podvignaroda.ru/Image3/newsearchservlet'
# json: 1

bot = Bot(token="5253505560:AAFlfKocSp0wANkP4q-E0Jum0yjSAh7vjhU")
# Объект бота @Heroicact_bot

dp = Dispatcher(bot)
# Диспетчер для бота

logging.basicConfig(level=logging.INFO)
# Включаем логирование, чтобы не пропустить важные сообщения
# ________________________________________________________________


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    buttons = ['Помощь', 'Билеты', 'Информация', 'Поклонка', 'Билеты']
    kbs = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbs.add(*buttons)
    await message.reply(f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=kbs)
# Приветствие


@dp.message_handler(Text(equals='Билеты'))
async def tickets(message: types.Message):
    buttons = [
        types.InlineKeyboardButton('Через сайт', url='https://victorymuseum.ru/for-visitors/prices/'),
        types.InlineKeyboardButton('Через Telegram')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Кинотеатр Поклонка подарит вам множество прекрасных эмоций!", reply_markup=keyboard)


@dp.message_handler(Text(equals='Поклонка'))
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton('Узнать больше о кинотеатре', url='https://victorymuseum.ru/for-visitors/kinoteatr/')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Кинотеатр Поклонка подарит вам множество прекрасных эмоций!", reply_markup=keyboard)


@dp.message_handler(Text(equals='Помощь'))
async def help(message: types.Message):
    await message.reply('''Функционал бота "Подвиг народа":\n/search [ФИО через пробел] - поиск человека по выбранным данным.\n/minfo - отображение основной информации о музее.''')
# Отклик на команду "help"


@dp.message_handler(commands="search")
async def cmd_test1(message: types.Message):
    search_string = message.get_args()
    # fetching urls will take some time, so notify user that everything is OK
    await types.ChatActions.typing()
    response = await search(search_string)
    # Send content
    pprint(response)
    if(response['result'] != 'OK'):
        await bot.send_message(message.chat.id, "Что-то пошло не так", parse_mode=ParseMode.MARKDOWN)
    else:
        persons = [person['f2'] + " " + person['f3'] + " " + person['f4'] + " " + person['f9'] for person in response['records']]
        await bot.send_message(message.chat.id,  emojize(text(*persons, sep='\n')), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(Text(equals='Информация'))
async def info(message: types.Message):
    buttons = [
        types.InlineKeyboardButton('Хотите узнать больше?', url='https://victorymuseum.ru/about/')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer(' Музей Победы — главный военно-исторический музей России по тематике Великой Отечественной и Второй мировой войн.', reply_markup=keyboard)
    # отклик на команду minfo (информация о музее)


async def search(search_string):    # Функция поиска людей
    xmlParam = f'<request firstRecordPosition="0" maxNumRecords="51" countResults="true">'
    xmlParam += f'<record fulltextfield="{search_string}" entity="Человек Награждение"></record>'
    xmlParam += f'<record fulltextfield="{search_string}" entity="Человек Представление"></record>'
    xmlParam += f'<record fulltextfield="{search_string}" entity="Человек Картотека"></record>'
    xmlParam += f'<record fulltextfield="{search_string}" entity="Человек Юбилейная Картотека"></record>'
    xmlParam += f'<record fulltextfield="{search_string}" entity="Человек Ин Картотека"></record>'
    xmlParam += '</request>'

    payload = {'json': 1, 'xmlParam': xmlParam}
    async with aiohttp.ClientSession() as session:
        async with session.post(REQUEST_API_URL, data=payload) as response:
            return await response.json()


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

# __________________________________________________
