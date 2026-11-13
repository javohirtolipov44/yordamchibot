import logging
from aiogram import Router, F, Bot
from aiogram.types import Message

router = Router()
logger = logging.getLogger(__name__)

@router.message(
    F.chat.type.in_({"group", "supergroup"}),
    F.new_chat_members | F.left_chat_member
)
async def delete_service_messages(message: Message, bot: Bot):
    """
    Guruhga a'zo qo'shilgan (o'zi kirgan yoki birov qo'shgan)
    yoki guruhdan chiqqan haqidagi servis xabarlarini o'chiradi.
    """
    try:
        await message.delete()
        if message.new_chat_members:
            names = ", ".join([u.full_name for u in message.new_chat_members])
            inviter = message.from_user.full_name if message.from_user else "Noma'lum"
            logger.info(f"Qo'shildi xabari o'chirildi: {inviter} -> {names} (Guruh: {message.chat.title})")
        else:
            left_user = message.left_chat_member.full_name if message.left_chat_member else "Noma'lum"
            logger.info(f"Chiqdi xabari o'chirildi: {left_user} (Guruh: {message.chat.title})")
    except Exception as e:
        logger.warning(
            f"Servis xabarini o'chirib bo'lmadi! Chat: {message.chat.title} (ID: {message.chat.id}, Type: {message.chat.type}). "
            f"Xatolik: {e}"
        )
        try:
            bot_member = await bot.get_chat_member(message.chat.id, bot.id)
            logger.warning(
                f"Botning guruhdagi statusi: {bot_member.status}. "
                f"can_delete_messages: {getattr(bot_member, 'can_delete_messages', None)}"
            )
        except Exception as check_err:
            logger.warning(f"Bot huquqini tekshirishda xatolik: {check_err}")


