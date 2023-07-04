

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_like = KeyboardButton('❤️')
button_next = KeyboardButton('Листать')

next_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=[
                                  [button_like, button_next]
                              ])