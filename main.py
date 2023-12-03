import asyncio
import logging
import threading

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import handlers
from handlers import router


async def main():
    bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=False)


if __name__ == "__main__":

    # threading.Thread(target=handlers.cur_pos).start()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
