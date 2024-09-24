import asyncio
import datetime

from aiogram import Router, Bot, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.repository import send_link_repository
from settings import send_link_photo_id
from utils.is_subscriber import is_subscriber

send_link_router = Router()


@send_link_router.callback_query(Text(startswith="start_send_link|"), any_state)
@is_subscriber
async def user_send_link(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    delete_message_id = int(message.data.split("|")[1])
    # user = Users(message.from_user.id, "send_link_data")
    # await user.read_data()
    # await user.add_user()
    user = await send_link_repository.get_user_by_user_id(message.from_user.id)
    if user is None:
        await send_link_repository.add_send_link(user_id=message.from_user.id, last_date_start=datetime.datetime.now())
    else:
        await send_link_repository.update_user_last_start_date_by_user_id(user_id=message.from_user.id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=delete_message_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="🧠 Изучить БАЗУ", url="https://t.me/slashstudy/37"))
    await message.message.answer_photo(caption=f"😉 Получи самую большую и топовую базу знаний по дизайну от студии Слеш, просто нажав кнопку",
                                       photo=send_link_photo_id, reply_markup=keyboard.as_markup())
    await asyncio.sleep(2)
    next_keyboard = InlineKeyboardBuilder()
    next_keyboard.row(InlineKeyboardButton(text="😎 Уже бегу", url="https://slashstudy.ru"))
    await message.message.answer(text=f"⭐ Мы хотим, чтобы ты становился лучше и придумали для тебя классно решение.\n\nПрокачивай свои скиллы в Слеш вместе с менторами из Ozon, Yandex, Сбер и других компаний, для этого забирай звонок с топом по скидке 30% до 20 апреля",
                                 reply_markup=next_keyboard.as_markup())