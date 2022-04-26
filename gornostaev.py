#!venv/bin/python
import logging
from pprint import pprint

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text

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
async def cmd_test1(message: types.Message):
    await message.reply('''Добро пожаловать, {new_member.mention}!
Для ознакомления с функционалом напишите "/help"''')
# Приветствие


@dp.message_handler(commands="help")
async def cmd_test1(message: types.Message):
    await message.reply('''Функционал бота "Подвиг народа":
/search [ФИО через пробел] - поиск человека по выбранным данным.
/minfo - отображение основной информации о музее.''')
# Отклик на команду "help"


@dp.message_handler(commands="search")
async def cmd_test1(message: types.Message):
    search_string = message.get_args()
    # fetching urls will take some time, so notify user that everything is OK
    await types.ChatActions.typing()
    response = await search(search_string)
    # Send content
    pprint(response)
    if response['result'] != 'OK':
        await bot.send_message(message.chat.id, "Что-то пошло не так", parse_mode=ParseMode.MARKDOWN)
    else:
        persons = [person['f2'] + " " + person['f3'] + " " + person['f4'] + " - " + person['f9'] for person in response['records']]
        await bot.send_message(message.chat.id,  emojize(text(*persons, sep='\n')), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands="minfo")
async def cmd_test1(message: types.Message):
    await message.reply('''Музей Победы — главный военно-исторический музей
России по тематике Великой Отечественной и Второй
мировой войн, один из крупнейших военно-исторических
музеев мира, общероссийский научно-исследовательский и
культурно-просветительский центр.
Сегодня музей является одним из ведущих институтов
противодействия попыткам фальсификации истории, а
также центром патриотического воспитания новых 
поколений.''')
    # отклик на команду minfo (информация о музее)


async def search(search_string):    # Функция поиска людей
    xmlParam = f'<request firstRecordPosition="0" maxNumRecords="20" countResults="true">'
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
