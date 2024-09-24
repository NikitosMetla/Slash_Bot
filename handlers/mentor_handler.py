import asyncio
import datetime

from aiogram import Router, Bot, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.repository import mentor_repository
from settings import send_link_photo_id, mentor_video_note
from utils.is_subscriber import is_subscriber

mentor_router = Router()


@mentor_router.callback_query(Text(startswith="mentor|"), any_state)
@is_subscriber
async def user_send_mentor(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    user = await mentor_repository.get_user_by_user_id(user_id=message.from_user.id)
    if user is None:
        await mentor_repository.add_mentor(user_id=message.from_user.id, last_date_start=datetime.datetime.now())
    else:
        await mentor_repository.update_user_last_start_date_by_user_id(user_id=message.from_user.id)
    await message.message.answer_video_note(video_note=mentor_video_note)
    await asyncio.sleep(3)
    link = '<a href="https://t.me/slashstudy">Слеш</a>'
    await message.message.answer(f'Этот бот создан ребятами из Слеш и дизайн-студии Вайт.\n\n{link} - это твой старший брат в дизайне. Ментор, задача которого реально помочь тебе стать круче')
    await asyncio.sleep(1.5)
    await message.message.answer("При этом не задолбать пушами и сухими ответами, а как настоящий друг: быть рядом, направлять на верный путь и поддерживать во время дороги")
    await asyncio.sleep(2)
    await message.message.answer('Сеньор и лид дизайнеры из Ozon, Yandex, СБЕР, МТС и других крупных компаний копнут в твои проблемы/хотелки и составят личный план развития в ноушене. По ходу пути все время будут с тобой отвечая на любые  вопросы, начиная от "Как создать компонент в фигме" заканчивая "Как забрать тендер с корпорацией"')
    await asyncio.sleep(2)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="🎁 Найти ментора", url="https://slashstudy.ru"))
    await message.message.answer("Я считаю, будет честно подарить тебе скидку на первую встречу - 30% до начала лета. Залетай на сайт, она уже ждет тебя)", reply_markup=keyboard.as_markup())