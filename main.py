"""
Основной модуль нашего телеграм-бота
"""
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import keyboards as kbs

#  @JC_telebot
token = '1794414260:AAHictDJ7hxUNIGSKtdLfbHnYCc9vWuV4eU'
bot = Bot(token=token, parse_mode='MarkdownV2')
dp = Dispatcher(bot, storage=MemoryStorage())

aviable_food = ['борщ', "гречка", "пельмени"]
aviable_sizes = ["большая", "средняя", "маленькая"]


class OrderFood(StatesGroup):
    waiting_for_food = State()
    waiting_for_size = State()


async def cancel_cmd(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отменено', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='start')
async def fnc_start(message: types.Message):
    await message.reply('Здравствуйте!')


async def food_start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in aviable_food:
        kb.add(name)
    await msg.answer('Выберите блюдо', reply_markup=kb)
    await OrderFood.waiting_for_food.set()


async def food_chosen(msg: types.Message, state: FSMContext):
    if msg.text.lower() not in aviable_food:
        await msg.answer('Выберите блюдо из списка')
        return
    await state.update_data(chosen_food=msg.text.lower())
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in aviable_sizes:
        kb.add(size)
    await OrderFood.next()
    await msg.answer('Выберите размер порции', reply_markup=kb)


async def food_size_chosen(msg: types.Message, state: FSMContext):
    if msg.text.lower() not in aviable_sizes:
        await msg.answer('Выберите размер из списка')
        return
    user_data = await state.get_data()
    await msg.answer(f'Вы выбрали {msg.text.lower()} порцию {user_data["chosen_food"]}',
                     reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands='menu')
async def user_menu(msg: types.Message):
    """
    Показывает меню кнопок для пользователя
    """
    await msg.answer('Что Вас интересует?', reply_markup=kbs.user_menu)


@dp.callback_query_handler(text='expo_info_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата: информация')


@dp.callback_query_handler(text='social_btn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата: Соцсети')

# ----------------------------------------------------------------------------  Зона администратора
async def user_is_admin(user_id) -> bool:
    """
    Проверяет является ли пользователь администраторром
    """
    return True  # Для тестов всегда возвращает True
    if user_id in {'1234567'}:
        return True
    return False


async def admin_menu(msg: types.Message):
    """
    Выводит меню для администратора
    """
    user_id = msg.from_user.id
    if not user_is_admin(user_id):
        await msg.answer('Это только для администраторов')
    else:
        txt = f'{user_id=}'
        await msg.answer(txt)


# -------------------------------------------------------------------  Зона регистрации событий-триггеров
dp.register_message_handler(cancel_cmd, commands='cancel', state='*')
dp.register_message_handler(food_start, commands='food', state="*")
dp.register_message_handler(food_chosen, state=OrderFood.waiting_for_food)
dp.register_message_handler(food_size_chosen, state=OrderFood.waiting_for_size)

dp.register_message_handler(admin_menu, commands='admin')

executor.start_polling(dp)
