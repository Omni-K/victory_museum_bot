from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

nokb = ReplyKeyboardRemove()

st_but = InlineKeyboardMarkup(row_width=1)
mn_but = InlineKeyboardButton('Открыть меню', callback_data='menu')
st_but.add(mn_but)

user_menu = InlineKeyboardMarkup(row_width=1)
expo_info_btn = InlineKeyboardButton('Часы работы и стоимость', callback_data='expo_info_btn')
social_btn = InlineKeyboardButton('Мы в соцсетях', callback_data='social_btn')
subscribe_btn = InlineKeyboardButton('Рассылка', callback_data='user_subscribe')
buytiket_btn = InlineKeyboardButton('Купить билеты', callback_data='buytikets')
podvig_btn = InlineKeyboardButton('Экспозиция "Подвиг народа"', callback_data='podvig_btn')
kino_btn = InlineKeyboardButton('Кинотеатр музея', callback_data='kino_btn')
user_menu.add(expo_info_btn,
              social_btn,
              subscribe_btn,
              buytiket_btn,
              podvig_btn,
              kino_btn,
              )

admin_menu = InlineKeyboardMarkup(row_width=1)
notify_btn = InlineKeyboardButton('Запустить рассылку новостей', callback_data='admin_notify')
admin_menu.add(notify_btn
               )

subscribe_yn = InlineKeyboardMarkup(row_width=1)
subscribe = InlineKeyboardButton('Подписаться', callback_data='subscribe')
unsubscribe = InlineKeyboardButton('Отписаться', callback_data='unsubscribe')
s_back = InlineKeyboardButton('Назад', callback_data='menu')
subscribe_yn.add(subscribe, unsubscribe, s_back)

tikets_kb = InlineKeyboardMarkup(row_width=1)
buy_in_tg = InlineKeyboardButton('Купить в телеграм', callback_data='buy_in_tg')
buy_on_site = InlineKeyboardButton('Купить на сайте', url='https://tickets.victorymuseum.ru/ru/#id=1')
tikets_kb.add(buy_in_tg, buy_on_site)

podvig_kb = InlineKeyboardMarkup(row_width=1)
url_podvig = InlineKeyboardButton('Прочитать об экспозиции',
                                  url='https://victorymuseum.ru/excursions/podvig-naroda/podvig-naroda/')
podvig_kb.add(url_podvig)

kino_kb = InlineKeyboardMarkup(row_width=1)
url_kino = InlineKeyboardButton('Узнать больше о кинотеатре',
                                  url='https://victorymuseum.ru/for-visitors/kinoteatr/')
kino_kb.add(url_kino)
