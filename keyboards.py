from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo


inline_kb_website = InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Открыть веб-страницу',
                                    web_app=WebAppInfo(url='https://www.poizonapp.com/'))],
    ])
