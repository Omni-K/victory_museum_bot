import logging
from aiogram import Bot, Dispatcher, executor, types

# @heroicact_bot
mytoken = '5253505560:AAFlfKocSp0wANkP4q-E0Jum0yjSAh7vjhU'

# Объект бота
bot = Bot(token=mytoken)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    txt = '''Введите имя, фамилию, отчество'''
    await message.answer(txt)


@dp.message_handler(commands=['send'])
async def notify_users(message: types.Message):
    print('*')
    with open("../user_ids.txt", "r") as file:
        for id in file.readlines():
            if id != '':
                await bot.send_message(id, 'ало')




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
