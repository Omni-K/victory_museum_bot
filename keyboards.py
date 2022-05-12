from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

nokb = ReplyKeyboardRemove()

user_menu = InlineKeyboardMarkup(row_width=1)
expo_info_btn = InlineKeyboardButton('Часы работы и стоимость', callback_data='expo_info_btn')
social_btn = InlineKeyboardButton('Мы в соцсетях', callback_data='social_btn')
subscribe_btn = InlineKeyboardButton('Подписаться на новости', callback_data='user_subscribe')

user_menu.add(expo_info_btn,
              social_btn,
              subscribe_btn,
              )

admin_menu = InlineKeyboardMarkup(row_width=1)
notify_btn = InlineKeyboardButton('Запустить рассылку новостей', callback_data='admin_notify')
admin_menu.add(notify_btn
               )

subscribe_yn = InlineKeyboardMarkup(row_width=1)
subscribe_yes = InlineKeyboardButton('Подписаться', callback_data='subscribe_yes')
subscribe_no = InlineKeyboardButton('Не подписываться', callback_data='subscribe_no')
subscribe_yn.add(subscribe_yes, subscribe_no)


# markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
# ).add(
#     KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
# )
#
# markup_big = ReplyKeyboardMarkup()
#
# markup_big.add(
#     button1, button2, button3, button4, button5, button6
# )
# markup_big.row(
#     button1, button2, button3, button4, button5, button6
# )
#
# markup_big.row(button4, button2)
# markup_big.add(button3, button2)
# markup_big.insert(button1)
# markup_big.insert(button6)
# markup_big.insert(KeyboardButton('9️⃣'))
#
#
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
#
# inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
# inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
# inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
# inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
# inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
# inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
# inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
# inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))
