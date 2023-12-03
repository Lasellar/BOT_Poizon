import time
from datetime import datetime
from math import ceil
import pyperclip
import requests
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import Command
from time import sleep
from random import random

from bs4 import BeautifulSoup
from selenium import webdriver
from pyautogui import moveTo, click, mouseDown, mouseUp, hotkey

import pyautogui
import threading

import config
import keyboards

router = Router()
pyautogui.FAILSAFE = False


class Review(StatesGroup):
    review_state = State()


class Product(StatesGroup):
    product_price_state = State()


class Order(StatesGroup):
    order_price = 0
    order_size = 0

    order_price_state_1 = State()
    order_price_state_2 = State()


customer = {}


def price(cny):
    with open('CURRENT_EXCHANGE_RATE.txt', 'r') as file:
        CURRENT_EXCHANGE_RATE = eval(file.read())
        print(CURRENT_EXCHANGE_RATE)
    # S=(O+6%)*K+3000, если O>=7000, то действуем по следующей формуле S=(O+7%)*K
    # S: sum
    # O: CNY
    # K: Current exchange rate
    print(cny, CURRENT_EXCHANGE_RATE)
    if cny < 7000:
        rub = ((cny * 1.06) * CURRENT_EXCHANGE_RATE) + 3000
    else:
        rub = (cny * 1.07) * CURRENT_EXCHANGE_RATE
    return ceil(rub)


r"""def cur_pos():
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(position_str, end='')
            time.sleep(0.3)
            print('\b' * len(position_str), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


def cursor():

    moveTo(1305, 261)
    sleep(8)

    mouseDown(button='left')
    sleep(0.26)
    moveTo(x=1306, y=353)
    sleep(0.2)
    mouseUp(button='left')

    sleep(random() * 3)
    moveTo(717, 460)
    sleep(2)

    mouseDown(button='left')
    sleep(0.9)
    moveTo(x=606, y=195)
    sleep(0.6)
    mouseUp(button='left')

    sleep(random() * 2 + 2)
    moveTo(718, 673)
    sleep(4)
    click()

    sleep(random() * 2 + 3)
    moveTo(438, 512)
    sleep(random() * 2)
    click()
    print("find x")
    moveTo(412, 541)
    sleep(15)

    mouseDown(button='left')
    sleep(0.6)
    moveTo(x=464, y=540)
    sleep(0.6)
    mouseUp(button='left')

    hotkey('ctrl', 'c', interval=1.1)
    print('ctrl c')
    print(f"скопировано {pyperclip.paste()}")
    if (len(pyperclip.paste()) == 5) or (len(pyperclip.paste()) == 4):
        with open('CURRENT_EXCHANGE_RATE.txt', 'w+') as rate:
            print("enter the 116")
            if "," in pyperclip.paste():
                price_cny = eval(pyperclip.paste().replace(",", "."))
            else:
                price_cny = eval(pyperclip.paste())
            print("write")
            rate.write(str(price_cny))
            print("written")
        _ = "-" * 10
        print(f'\n{_}\nТекущая стоимость: {price_cny}\n{_}\n')"""


def rate_parcer():
    url = "https://www.banki.ru/products/currency/bank/sberbank/moskva/#bank-rates"
    page = requests.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    allas = str(soup.findAll(name='td', class_='font-size-large'))[1:-1]
    counties = allas.split(sep='\n\t\t\t\t\t\t</td>, <td class="font-size-large">\n\t\t\t\t\t\t\t')
    print(f"ilist: {counties}")
    current_count = counties[19].replace(',', '.')
    print(f"current exchange rate= {current_count}")

    with open('CURRENT_EXCHANGE_RATE.txt', 'w') as rate:
        print("enter the 145")
        rate.write(str(current_count))
        print("written")


"""def parcer():
    print('vhod v parcer')
    # driver = webdriver.Chrome()
    # print('chrome')
    # driver.get('http://www.sberbank.ru/ru/quotes/currencies?currency=CNY')
    thread = threading.Thread(target=rate_parcer)
    thread.start()
    #sleep(75)"""


def time_check():
    while True:
        sleep(1)
        current_datetime = datetime.now()
        timenow_hour = str(current_datetime.hour)
        timenow_minute = str(current_datetime.minute)
        timenow_second = str(current_datetime.second)
        if len(timenow_hour) != 2:
            timenow_hour = "0" + timenow_hour
        if len(timenow_minute) != 2:
            timenow_minute = "0" + timenow_minute
        if len(timenow_second) != 2:
            timenow_second = "0" + timenow_second
        timenow = timenow_hour + timenow_minute + timenow_second
        timenow_display = f"{timenow_hour}:{timenow_minute}:{timenow_second}"
        if timenow in config.timenows:
            print(f"{timenow_display} starting the process of updating the current course")
            threading.Thread(target=rate_parcer).start()
            sleep(1)


threading.Thread(target=time_check).start()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [keyboards.inline_kb_currency],
        [keyboards.inline_kb_order_currency],
        [keyboards.inline_kb_review]
    ])
    text = "Привет, это Poizoner!\n Spiremsu_bot поможет рассчитать стоимость товара c доставкой до Москвы."
    await msg.answer(text=text, reply_markup=markup)


@router.message(Review.review_state)
async def review_forward(msg: Message, state: FSMContext):
    await state.clear()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [keyboards.inline_kb_currency],
        [keyboards.inline_kb_review]
    ])
    await msg.reply(text="Отзыв отправлен!", reply_markup=markup)
    await msg.forward(chat_id=-1001705244941)


@router.message(Product.product_price_state)
async def echo_message(msg: Message, state: FSMContext):
    await state.clear()
    print(f"recieved message from {msg.from_user.id}: {msg.text}")
    try:
        if ',' in msg.text:
            price_in_cny = eval(msg.text.replace(",", "."))
        else:
            price_in_cny = eval(msg.text)
        price_in_rub = price(price_in_cny)
        markup = InlineKeyboardMarkup(inline_keyboard=[[keyboards.inline_kb_back]])
        text_order = (f'Сумма заказа составит {price_in_rub} RUB. Срок доставки 14-20 дней.\n'
                      f'Для заказа писать <a href="https://t.me/zakaz_poizoner">Poizoner</a>')
        await msg.answer(text=text_order, reply_markup=markup, parse_mode="HTML")
    except (NameError, SyntaxError, TypeError):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_currency],
            [keyboards.inline_kb_review]
        ])
        text = "Пожалуйста, отправь сообщение только из числовых символов, чтобы я смог рассчитать стоимость в рублях"
        await msg.answer(text=text, reply_markup=markup)


@router.message(Order.order_price_state_1)
async def echo_message(msg: Message, state: FSMContext):
    global customer
    print(customer)
    print(f"recieved message from {msg.from_user.id}: {msg.text}")
    try:
        if ',' in msg.text:
            price_in_cny = eval(msg.text.replace(",", "."))
        else:
            price_in_cny = eval(msg.text)
        customer[str(msg.from_user.id)] = {}
        customer[str(msg.from_user.id)]["order_price"] = price_in_cny
        markup = InlineKeyboardMarkup(inline_keyboard=[[keyboards.inline_kb_back]])
        await msg.answer(text=config.text_order_cost_calc_2, reply_markup=markup)
        await state.set_state(Order.order_price_state_2)
    except (NameError, SyntaxError, TypeError):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_review],
            [keyboards.inline_kb_back]
        ])
        text = "Пожалуйста, отправь сообщение только из числовых символов, чтобы я смог рассчитать стоимость в рублях"
        await msg.answer(text=text, reply_markup=markup)


@router.message(Order.order_price_state_2)
async def echo_message_2(msg: Message, state: FSMContext):
    global customer
    # S = (H + 6 %) * K + V * 2050
    # S = стоимость, ответ
    # H - общая стоимость корзины
    # K - курс
    # V - количество позиций
    print(f"recieved message from {msg.from_user.id}: {msg.text}")
    try:
        if ',' in msg.text:
            price_in_cny = eval(msg.text.replace(",", "."))
        else:
            price_in_cny = eval(msg.text)
        customer[str(msg.from_user.id)]["order_size"] = price_in_cny
        markup = InlineKeyboardMarkup(inline_keyboard=[[keyboards.inline_kb_back]])
        H = customer[str(msg.from_user.id)]["order_price"]
        with open('CURRENT_EXCHANGE_RATE', 'r') as file:
            K = eval(file.read())
        V = customer[str(msg.from_user.id)]["order_size"]
        S = ((H * 1.06) * K) + (V * 2050)
        text = (f'Сумма заказа составит {ceil(S)} RUB. Срок доставки 14-20 дней.\n'
                f'Для заказа писать <a href="https://t.me/zakaz_poizoner">Poizoner</a>')
        await msg.answer(text=text,
                         reply_markup=markup,
                         parse_mode="HTML")
        await state.clear()
        customer = {}
    except (NameError, SyntaxError, TypeError):
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_review],
            [keyboards.inline_kb_back]
        ])
        text = ("Пожалуйста, отправь сообщение только из числовых символов,"
                " чтобы я смог корректно рассчитать стоимость")
        await msg.answer(text=text, reply_markup=markup)


@router.callback_query()
async def answer(call, state: FSMContext):
    if call.data == "Рассчитать цену одного товара":
        await state.set_state(Product.product_price_state)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_back]
        ])
        await call.message.edit_text(text=config.text_product_cost_calc, reply_markup=markup)

    if call.data == "Рассчитать стоимость заказа":
        await state.set_state(Order.order_price_state_1)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_back]
        ])
        await call.message.edit_text(text=config.text_order_cost_calc_1, reply_markup=markup)

    if call.data == "Назад":
        await state.set_state(None)
        user_data = await state.get_data()
        print(user_data)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_currency],
            [keyboards.inline_kb_order_currency],
            [keyboards.inline_kb_review]
        ])
        await call.message.edit_text(text="Привет!", reply_markup=markup)

    if call.data == "Оставить отзыв":
        await state.set_state(Review.review_state)
        text = ("Хотите оставить отзыв?\nОтправьте его одним сообщением и приложите к нему скриншот/видео, если "
                "имеется. Пожалуйста, не прикрепляйте к сообщению больше 1 медиафайла")
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [keyboards.inline_kb_back]
        ])
        await call.message.edit_text(text=text, reply_markup=markup)



@router.message()
async def new_rate_command(msg: Message):
    if "///юааань новый курс сейчас " in msg.text:
        with open('CURRENT_EXCHANGE_RATE', 'w+') as rate:
            rate.write(msg.text[-5:])

