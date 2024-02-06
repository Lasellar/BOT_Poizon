from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import keyboards
router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Это магазин POIZON. Ты можешь открыть наше приложение, чтобы посмотреть товары.",
                     reply_markup=keyboards.inline_kb_website)
