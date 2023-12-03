from aiogram.types import InlineKeyboardButton

inline_kb_currency = InlineKeyboardButton(text='Рассчитать цену одного товара',
                                          callback_data='Рассчитать цену одного товара')
inline_kb_order_currency = InlineKeyboardButton(text='Рассчитать стоимость заказа',
                                                callback_data='Рассчитать стоимость заказа')
inline_kb_review = InlineKeyboardButton(text='Оставить отзыв', callback_data='Оставить отзыв')
inline_kb_back = InlineKeyboardButton(text="Назад", callback_data='Назад')
