import re
import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.enums import MessageEntityType
from aiogram.types import Message
from utils.admin_check import is_admin

router = Router()
logger = logging.getLogger(__name__)

# Havolalarni aniqlash uchun muntazam ifoda (regex)
SPAM_URL_PATTERN = re.compile(
    r"(https?://\S+|t\.me/\S+|telegram\.me/\S+|telegram\.dog/\S+|www\.\S+|bit\.ly/\S+|[a-zA-Z0-9-]+\.(?:com|ru|uz|net|org|io|me|info)(?:/\S*)?)",
    re.IGNORECASE
)

# Telegram username / kanal yozuvlarini aniqlash (@kanal_nomi)
MENTION_PATTERN = re.compile(r"@[a-zA-Z0-9_]{4,}", re.IGNORECASE)


def check_is_ad(message: Message) -> bool:
    """
    Xabarda reklama, havola yoki kanaldan forward qilingan post
    borligini tekshiradi.
    """
    # 1. Kanaldan forward qilingan xabarlarni tekshirish
    if message.forward_origin and getattr(message.forward_origin, "type", None) == "channel":
        return True
    if message.forward_from_chat and getattr(message.forward_from_chat, "type", None) == "channel":
        return True

    # 2. Xabar matni yoki rasm/video ostidagi izoh (caption)
    text = message.text or message.caption or ""

    if SPAM_URL_PATTERN.search(text) or MENTION_PATTERN.search(text):
        return True

    # 3. Telegram entities (yashirin va to'g'ridan-to'g'ri havolalar)
    entities = (message.entities or []) + (message.caption_entities or [])
    for entity in entities:
        if entity.type in (
            MessageEntityType.URL,
            MessageEntityType.TEXT_LINK,
            MessageEntityType.MENTION,
        ):
            return True

    return False


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def filter_spam_messages(message: Message, bot: Bot):
    """
    Guruhdagi reklama xabarlarini aniqlaydi va o'chiradi.
    Adminlarning xabarlariga tegilmaydi.
    """
    # Agar reklama alomatlari bo'lmasa, e'tiborsiz qoldiramiz
    if not check_is_ad(message):
        return

    # Guruh admini yoki egasi bo'lsa, xabar o'chirilmaydi
    if await is_admin(bot, message):
        return

    try:
        # Reklama xabarini o'chirish
        await message.delete()

        user_name = message.from_user.full_name if message.from_user else "Foydalanuvchi"
        logger.info(f"Reklama o'chirildi: {user_name} ({message.chat.title})")

        # Ogohlantirish xabari yuborish va 5 soniyadan so'ng o'chirib yuborish (chat tozalanadi)
        warning_msg = await message.answer(
            f"⚠️ <b>{user_name}</b>, guruhda reklama yoki havola tarqatish taqiqlangan!",
            parse_mode="HTML"
        )
        await asyncio.sleep(5)
        await warning_msg.delete()

    except Exception as e:
        logger.error(f"Reklamani o'chirishda xatolik: {e}")

