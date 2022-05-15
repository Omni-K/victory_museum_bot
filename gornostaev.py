import logging
from pprint import pprint
import keyboards as kbs
import requests
from bs4 import BeautifulSoup
import json

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import Text


# ________________________________________________________________
REQUEST_API_URL = 'http://podvignaroda.ru/Image3/newsearchservlet'
# json: 1

bot = Bot(token="5253505560:AAFlfKocSp0wANkP4q-E0Jum0yjSAh7vjhU")
# Объект бота @Heroicact_bot

dp = Dispatcher(bot, storage=MemoryStorage())
# Диспетчер для бота

logging.basicConfig(level=logging.INFO)
# Включаем логирование, чтобы не пропустить важные сообщения
# ________________________________________________________________


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply(f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=kbs.st_but)
# Приветствие


@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Что вас интересует?', reply_markup=kbs.user_menu)
# Меню


@dp.message_handler(Text(equals='Билеты'))
async def tickets(message: types.Message):
    buttons = [
        types.InlineKeyboardButton('Через сайт', url='https://victorymuseum.ru/for-visitors/prices/'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Билеты", reply_markup=keyboard)


@dp.callback_query_handler(text='kino_btn')
async def cinema(callback_query: types.CallbackQuery):
    def get_cin():
        headers = {
            'user-agent': 'Mozilla:/5.0(Windows NT 10.0; Win64; x64; rv: 100.0) Gecko/20100101 Firefox/100.0'
        }
        url = 'https://victorymuseum.ru/for-visitors/kinoteatr/'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        url_cards = soup.find_all('a', class_='img-box')
        article_cards = soup.find_all('div', class_='text-box')
        ls_url = []
        ls_name = []
        ls = []
        for article in url_cards:
            article_url = article.get('href')
            ls_url.append(article_url)
        for article in article_cards:
            article_name = article.find('a', class_='name')
            if article_name is not None:
                ls_name.append(article_name)
        for i in ls_name:
            x = str(i).split('>')
            q = ''.join(x[1])
            ls.append(q[:-3])
        return [ls_url[:4], ls[:4]]

    buttons = [
        types.InlineKeyboardButton(get_cin()[1][u], url=get_cin()[0][u]) for u in range(4)
    ]
    buttons.append(types.InlineKeyboardButton('Узнать больше о кинотеатре', url='https://victorymuseum.ru/for-visitors/kinoteatr/'))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id, 'Список фильмов', reply_markup=keyboard)


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

@dp.callback_query_handler(text='user_subscribe')
async def yn(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Согласитесь на подписку', reply_markup=kbs.subscribe_yn)


@dp.callback_query_handler(text='subscribe')
async def subscribe(callback_query: types.CallbackQuery):
    userid = str(callback_query.from_user.id)
    with open("user_ids.txt", "r") as file:
        if userid in file.read():
            await bot.send_message(callback_query.from_user.id, 'Упс, Вы уже подписаны на рассылку.')
        else:
            with open("user_ids.txt", "a+") as file:
                file.write(userid + "\n")
                await bot.send_message(callback_query.from_user.id, 'Вы подписались на рассылку!')


@dp.callback_query_handler(text='unsubscribe')
async def unsubscribe(callback_query: types.CallbackQuery):
    userid = str(callback_query.from_user.id)
    with open("user_ids.txt", "r") as file:
        if userid not in file.read():
            await bot.send_message(callback_query.from_user.id, 'Вы не были подписаны на рассылку.')
        else:
            f = open("user_ids.txt", "a+")
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != user_id:
                    f.write(i)
            f.truncate()
            f.close()
            await bot.send_message(callback_query.from_user.id, 'Вы отписались от рассылки.',)


@dp.callback_query_handler(text='menu')
async def s_back(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Что вас интересует?', reply_markup=kbs.user_menu)
#-----------------------------------


@dp.message_handler(commands=['send'])
async def notify_users(message: types.Message):
    print('*')
    with open("user_ids.txt", "r") as file:
        for id in file.readlines():
            if id != '':
                await bot.send_message(id, 'ало')



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

# __________________________________________________
