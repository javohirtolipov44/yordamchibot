import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from handlers import register_handlers

# Loglarni sozlash - faqat xatoliklar (ERROR) chiqadi
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
# Aiogram va asyncio kutubxonalari loglarini ham faqat ERROR darajasiga o'rnatish
logging.getLogger("aiogram").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


ADMIN_ID = 1179777869


async def startup_answer(bot: Bot):
    try:
        await bot.send_message(ADMIN_ID, "Bot ishga tushdi✅")
    except Exception as e:
        logger.error(f"Startup xabarini yuborib bo'lmadi: {e}")


async def shutdown_answer(bot: Bot):
    try:
        await bot.send_message(ADMIN_ID, "Bot to'xtadi❌")
    except Exception as e:
        logger.error(f"Shutdown xabarini yuborib bo'lmadi: {e}")


async def main():
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "XATOLIK: BOT_TOKEN ko'rsatilmagan! "
            ".env faylini ochib, BotFather bergan tokenni kiriting."
        )
        return

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Handlerlarni ro'yxatdan o'tkazish
    register_handlers(dp)

    # Bot yoqilganda va o'chganda xabar yuborish hodisalari (Startup & Shutdown)
    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)

    # Bot o'chirilgan vaqtda yig'ilib qolgan eski xabarlarni o'tkazib yuborish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

