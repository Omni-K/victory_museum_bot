import logging
from pprint import pprint

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards_gor as kbs
import requests
from bs4 import BeautifulSoup
import json
import lxml
#   @Heroicact_bot

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import Text
from aiogram.types.base import String


# ________________________________________________________________
# Объект бота @Heroicact_bot


token_hero = "5253505560:AAFlfKocSp0wANkP4q-E0Jum0yjSAh7vjhU"
bot = Bot(token=token_hero)
dp = Dispatcher(bot, storage=MemoryStorage())

class NotifyOrder(StatesGroup):
    waiting_for_msg = State()
    waiting_for_confirm = State()
# Диспетчер для бота

logging.basicConfig(level=logging.INFO)
# Включаем логирование, чтобы не пропустить важные сообщения
# ________________________________________________________________

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    msg_text = f'Добро пожаловать, {message.from_user.first_name}!\nЭто бот Музея Победы.\nВы можете использовать команду \\menu для вызова основного меню пользователя '
    await message.reply(msg_text, reply_markup=kbs.st_but)
# Приветствие
# ________________________________________________________________
@dp.message_handler(commands='menu')
async def men(message: types.Message):
    await message.reply('Что вас интересует?', reply_markup=kbs.user_menu)

@dp.callback_query_handler(text='menu')
async def menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Что вас интересует?', reply_markup=kbs.user_menu)
# Меню
# ________________________________________________________________

@dp.callback_query_handler(text='social_btn')
async def menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Мы в социальных сетях:', reply_markup=kbs.soc_kb)
# Социальные сети
# ________________________________________________________________

@dp.callback_query_handler(text='expo_info_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Что вас интересует?', reply_markup=kbs.expo_kb)
# Меню выставок
# ________________________________________________________________


@dp.callback_query_handler(text='expos_link')
async def process_callback_button1(callback_query: types.CallbackQuery):

    def get_expo():
        headers = {
            'user-agent': 'Mozilla:/5.0(Windows NT 10.0; Win64; x64; rv: 100.0) Gecko/20100101 Firefox/100.0'
        }
        url = 'https://victorymuseum.ru/museum-complex/glavnoe-zdanie-muzeya/'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        cards = soup.find_all('div', class_='column_box__title')
        ls_url = []
        ls_name = []
        ls = []
        for j in cards:
            url_cards = j.find_all('a')
            for url in url_cards:
                article_url = url.get('href')
                if article_url not in ls_url:
                    print(article_url)
                    ls_url.append('https://victorymuseum.ru' + article_url)
            for article in url_cards:
                article_name = article
                if article_name is not None:
                    ls_name.append(article_name)
            for i in ls_name:
                x = str(i).split('>')
                q = ''.join(x[1])
                if q[:-3] not in ls:
                    ls.append(q[:-3])
        ln = len(ls_url)
        return [ls_url[:ln], ls[:ln], ln]

    buttons = [
        types.InlineKeyboardButton(get_expo()[1][u], url=get_expo()[0][u]) for u in range(get_expo()[2])
    ]
    buttons.append(types.InlineKeyboardButton('Больше выставок', url='https://victorymuseum.ru/museum-complex/glavnoe-zdanie-muzeya/'))
    buttons.append(kbs.t_back)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id, 'Рекомендуем посетить', reply_markup=keyboard)


@dp.callback_query_handler(text='buytikets')
async def buytikets(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Выберите удобный для вас способ покупки',
                           reply_markup=kbs.tikets_kb)


@dp.callback_query_handler(text='kino_btn')
async def cinema(callback_query: types.CallbackQuery):

    def get_cin():
        headers = {
            'user-agent': 'Mozilla:/5.0(Windows NT 10.0; Win64; x64; rv: 100.0) Gecko/20100101 Firefox/100.0'
        }
        url = 'https://poklonka-cinema.ru/films/'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        cards = soup.find_all('div', id='s1', class_='seance-elem')
        ls_url = []
        ls_name = []
        ls = []
        ls_time = []
        lst = []
        for j in cards:
            url_cards = j.find_all('a', class_='item')
            for url in url_cards:
                article_url = url.get('href')
                ls_url.append(article_url)
            for article in url_cards:
                article_name = article.find('div', class_='name')
                if article_name is not None:
                    ls_name.append(article_name)
            for i in ls_name:
                x = str(i).split('>')
                q = ''.join(x[1])
                ls.append(q[:-5])
            for time in url_cards:
                article_time = time.find('div', class_='value')
                if article_time is not None:
                    ls_time.append(article_time)
            for i in ls_time:
                x = str(i).split('>')
                q = ''.join(x[1])
                z = len(q) - 5
                lst.append(q[:-z])
        ln = len(ls_url)
        if ln > 0:
            return [[ls_url[:ln], ls[:ln], lst[:ln]], ln]
        return 'Сегодня фильмов нет :('

    if type(get_cin()) == str:
        buttons = []
    else:
        buttons = [
            types.InlineKeyboardButton(get_cin()[0][2][u] + ': ' + get_cin()[0][1][u], url=get_cin()[0][0][u]) for u in range(get_cin()[1])
        ]
    buttons.append(types.InlineKeyboardButton('Узнать больше о кинотеатре', url='https://victorymuseum.ru/for-visitors/kinoteatr/'))
    buttons.append(kbs.t_back)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    if type(get_cin()) == str:
        await bot.send_message(callback_query.from_user.id, get_cin(), reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, 'Сегодня в репертуре:', reply_markup=keyboard)


@dp.callback_query_handler(text='mus_info')
async def info(callback_query: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton('Хотите узнать больше?', url='https://victorymuseum.ru/about/')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(kbs.s_back)
    await bot.send_message(callback_query.from_user.id, 'Музей Победы — главный военно-исторический музей России по тематике Великой Отечественной и Второй мировой войн.', reply_markup=keyboard)
    # отклик на команду minfo (информация о музее)
#________________________________________________________

@dp.callback_query_handler(text='user_subscribe')
async def yn(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Хотите ли вы подписаться?', reply_markup=kbs.subscribe_yn)


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
    user_id = str(callback_query.from_user.id)
    with open("user_ids.txt", "r") as file:
        if user_id not in file.read():
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


#-----------------------------------
async def user_is_admin(user_id) -> bool:
    """
    Проверяет является ли пользователь администраторром
    """
    admin_ids = ['902834713', '673596786']
    return True  # Для тестов всегда возвращает True
    if str(user_id) in admin_ids:
        return True
    return False


@dp.message_handler(commands=['admin'])
async def admin_menu(msg: types.Message):
    """
    Выводит меню для администратора
    """
    user_id = msg.from_user.id
    if not user_is_admin(user_id):
        await msg.answer('Это только для администраторов')
    else:
        txt = 'Меню администратора' #f'{msg.from_user.first_name}'
        await msg.answer(txt, reply_markup=kbs.admin_menu)


@dp.callback_query_handler(text='admin_notify')
async def notify(message: types.Message):
    await message.answer('Введите сообщение, которое будет отправлено всем подписавшимся\, после подтверждения')
    await NotifyOrder.waiting_for_msg.set()


async def wait_for_msg_fnc(msg: types.Message, state: FSMContext):
    await state.update_data(txt=msg.text)
    await NotifyOrder.next()
    kbyn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbyn.add('Да', 'Нет')
    await msg.answer('Отправить это сообщение подписчикам?', reply_markup=kbyn)

async def send_notify_fnc(msg: types.Message, state: FSMContext):
    if msg.text.lower() == 'да':
        txt_to_send = await state.get_data()
        mes = txt_to_send['txt']
        sent = 0
        with open('user_ids.txt') as ids:
            for line in ids:
                user_id = int(line.strip())
                try:
                    await bot.send_message(user_id, mes, parse_mode='', reply_markup=types.ReplyKeyboardRemove())
                    sent += 1
                except Exception:
                    pass
        await msg.answer(f'Рассылка завершена. Отправлено сообщений: {sent}', parse_mode='',
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        await msg.answer('Отправка отменена', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

async def cancel_cmd(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отменено', reply_markup=types.ReplyKeyboardRemove())

async def shutdown_fnc(msg: types.Message):
    await msg.answer('Выключаю бота')
    import sys
    sys.exit()

dp.register_message_handler(shutdown_fnc, commands='shutdown')
dp.register_message_handler(cancel_cmd, commands='cancel')
dp.register_message_handler(wait_for_msg_fnc, state=NotifyOrder.waiting_for_msg)
dp.register_message_handler(send_notify_fnc, state=NotifyOrder.waiting_for_confirm)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

# __________________________________________________
