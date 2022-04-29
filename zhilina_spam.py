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
    with open("user_ids.txt", "r") as file:
        for id in file.readlines():
            if id != '':
                await bot.send_message(id, 'ало')

@dp.message_handler(commands='news')
async def yn(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'Да'
    btn2 = 'Нет'
    kb.add(btn1)
    kb.add(btn2)
    await message.answer(
        'Нажимая функцию /news, вы соглашаетесь на рассылку новостей. Если Вы согласны, нажмите да, иначе - нет',
        reply_markup=kb)


@dp.message_handler()
async def main(message: types.Message):
    nokb = types.ReplyKeyboardRemove()
    userid = str(message.from_user.id)

    if message.text == 'Да':
        allreadyexist = False
        with open("user_ids.txt", "r") as file:
            if userid in file.read():
                allreadyexist = True
        if allreadyexist:
            await message.answer('Упс, Вы уже подписаны на рассылку', reply_markup=nokb, parse_mode='MarkdownV2')
        else:
            with open("user_ids.txt", "a+") as file:
                file.write(userid + "\n")
                await message.answer('Вы подписались на рассылку\!', reply_markup=nokb, parse_mode='MarkdownV2')
    elif message.text == 'Нет':
        return



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
