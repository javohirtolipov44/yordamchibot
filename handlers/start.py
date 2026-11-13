from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart(), F.chat.type == "private")
async def start_private(message: Message):
    text = (
        "👋 <b>Assalomu alaykum! JAVOHIR</b>\n\n"
        "Men guruhlarni tozalovchi va nazorat qiluvchi yordamchi botman.\n\n"
        "<b>Mening vazifalarim:</b>\n"
        "• 🗑 Guruhga a'zo qo'shildi / chiqdi xabarlarini avtomatik o'chirish\n"
        "• 🚫 Reklama, havolalar (linklar) va kanaldan uzatilgan (forward) xabarlarni tozalash\n\n"
        "<b>Botni ishlatish uchun:</b>\n"
        "1. Meni guruhingizga qo'shing\n"
        "2. Menga guruhda <b>Administrator</b> huquqini bering (ayniqsa, <i>Xabarlarni o'chirish</i> huquqi kerak)"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("help"))
async def help_cmd(message: Message):
    text = (
        "ℹ️ <b>Yordam:</b>\n\n"
        "Bot to'g'ri ishlashi uchun uni guruhga admin qilib tayinlang va <b>Xabarlarni o'chirish</b> (Delete messages) ruxsatini bering.\n"
        "Bot guruh adminlarining xabarlariga tegmaydi."
    )
    await message.answer(text, parse_mode="HTML")

