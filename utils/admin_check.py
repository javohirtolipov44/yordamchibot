import logging
from aiogram import Bot
from aiogram.types import Message

logger = logging.getLogger(__name__)

async def is_admin(bot: Bot, message: Message) -> bool:
    """
    Xabar yuboruvchisi guruh admini yoki egasi ekanligini tekshiradi.
    Agar admin bo'lsa True, oddiy foydalanuvchi bo'lsa False qaytaradi.
    """
    # Anonim admin tekshiruvi (guruh nomidan yozgan admin)
    if message.sender_chat and message.sender_chat.id == message.chat.id:
        return True

    # Agar xabar foydalanuvchisi aniqlanmasa (masalan, kanaldan avtomatik bog'langan post)
    if not message.from_user:
        return False

    try:
        member = await bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        return member.status in ("creator", "administrator")
    except Exception as e:
        logger.error(f"Adminlik huquqini tekshirishda xatolik: {e}")
        return False

