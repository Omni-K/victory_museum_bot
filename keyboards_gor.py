from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
import unicodedata

nokb = ReplyKeyboardRemove()

s_back = InlineKeyboardButton('Вернуться в меню', callback_data='menu')
st_but = InlineKeyboardMarkup(row_width=1)
mn_but = InlineKeyboardButton('Открыть меню', callback_data='menu')
st_but.add(mn_but)

user_menu = InlineKeyboardMarkup(row_width=1)
mus_info = InlineKeyboardButton('О музее', callback_data='mus_info')
expo_info_btn = InlineKeyboardButton('Что посетить?', callback_data='expo_info_btn')
social_btn = InlineKeyboardButton('Мы в соцсетях', callback_data='social_btn')
subscribe_btn = InlineKeyboardButton('Управление рассылкой', callback_data='user_subscribe')
search_btn = InlineKeyboardButton('Узнать о родственниках-ветеранах',
                                  url='https://pamyat-naroda.ru/heroes/?static_hash=c29709454e0e4b2f379603cd966af235v9')
user_menu.add(mus_info,
              expo_info_btn,
              social_btn,
              subscribe_btn,
              search_btn,
              )


admin_menu = InlineKeyboardMarkup(row_width=1)
notify_btn = InlineKeyboardButton('Запустить рассылку новостей', callback_data='admin_notify')
admin_menu.add(notify_btn
               )


subscribe_yn = InlineKeyboardMarkup(row_width=1)
subscribe = InlineKeyboardButton('Подписаться', callback_data='subscribe')
unsubscribe = InlineKeyboardButton('Отписаться', callback_data='unsubscribe')
subscribe_yn.add(subscribe, unsubscribe, s_back)

tikets_kb = InlineKeyboardMarkup(row_width=1)
buy_on_site = InlineKeyboardButton('Купить на сайте', url='https://tickets.victorymuseum.ru/ru/#id=1')
t_back = InlineKeyboardButton('Вернуться назад', callback_data='expo_info_btn')
tikets_kb.add(buy_on_site, t_back)


expo_kb = InlineKeyboardMarkup(row_width=1)
expos_link = InlineKeyboardButton('Наши выставки', callback_data='expos_link')
kino_btn = InlineKeyboardButton('Кинотеатр музея', callback_data='kino_btn')
buytiket_btn = InlineKeyboardButton('Купить билеты', callback_data='buytikets')
expo_kb.add(expos_link, buytiket_btn, kino_btn, s_back)

soc_kb = InlineKeyboardMarkup(row_width=1)
ut = InlineKeyboardButton('Наш Youtube', url='https://www.youtube.com/channel/UCfJd9RT4pg_CckntWhlhH0w')
rut = InlineKeyboardButton('Наш Rutube', url='https://rutube.ru/channel/24766128/')
vk = InlineKeyboardButton('Наш VKонтакте', url='https://vk.com/muzeypobedy')
odn = InlineKeyboardButton('Наши Одноклассники', url='https://ok.ru/group/53681227104435')
zen = InlineKeyboardButton('Наш Yandex Zen', url='https://zen.yandex.ru/muzeypobedy')
soc_kb.add(ut, rut, vk, odn, zen, s_back)
