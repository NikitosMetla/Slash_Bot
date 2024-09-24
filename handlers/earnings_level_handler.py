import asyncio
import datetime
import random

from aiogram import Router, Bot, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.repository import earnings_level_repository
from settings import earnings_questions, InputMessage, options, stickers, earnings_level_photo_id, user_earning, \
    design_level_video_note2, mentor_video_note, level_photos, user_earning_photos
from utils.is_subscriber import is_subscriber

earnings_level_router = Router()


@earnings_level_router.callback_query(Text(startswith="start_earnings_level|"), any_state)
@is_subscriber
async def user_send_link(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    delete_message_id = int(message.data.split("|")[1])
    # user = Users(message.from_user.id, "earnings_level")
    # await user.read_data()
    # await user.add_user()
    user = await earnings_level_repository.get_user_by_user_id(user_id=int(message.from_user.id))
    if user is None:
        await earnings_level_repository.add_earnings_level(user_id=message.from_user.id, finish_service=False,
                                                           last_date_start=datetime.datetime.now())
    else:
        await earnings_level_repository.update_user_last_start_date_by_user_id(user_id=int(message.from_user.id))
        if user.finish_service:
            await earnings_level_repository.update_finish_service_by_user_id(user_id=int(message.from_user.id))
    keyboard = InlineKeyboardBuilder()
    question = earnings_questions.get('1 вопрос')
    for i, answer in enumerate(question.get("answers").keys()):
        keyboard.row(
            InlineKeyboardButton(text=options[i], callback_data=f"answer|{question.get('answers').get(answer)}|"
                                                                f"{1}"))
    answers = list(question.get("answers").keys())
    random.shuffle(answers)
    for i in range(len(answers)):
        answers[i] = f"{stickers[i]} {answers[i]}"
    text = (f"{1}."
            f" {question.get('content')}") + "\n    " + "\n    ".join(answers)
    await message.message.answer_photo(caption="Да начнется же тест <b>«Сколько ты зарабатываешь?»</b>!\n\nОтветив всего на десять вопросов узнаешь, насколько ты богатый котик",
                                       photo=earnings_level_photo_id)
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=delete_message_id)
    await message.message.answer(text=text, reply_markup=keyboard.as_markup())
    await state.set_state(InputMessage.earning_level)
    await state.update_data(last_question=1)


@earnings_level_router.callback_query(Text(startswith="answer|"), InputMessage.earning_level)
@is_subscriber
async def user_send_link(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = call.data.split("|")[1:]
    last_answer, last_question = int(data[0]), int(data[1])
    points = await state.get_data()
    if points.get("last_question") is None or (int(points.get("last_question")) != last_question):
        return
    points[str(last_question)] = last_answer
    points["last_question"] = last_question + 1
    await state.update_data(points)
    if last_question == 10:
        # user = Users(call.from_user.id, "earnings_level")
        # await user.read_data()
        # await user.edit_completion()
        await earnings_level_repository.update_finish_service_by_user_id(user_id=int(call.from_user.id))
        final_points = sum(points.values()) - int(points.get("last_question"))
        level = ""
        level_photo = ""
        for key in user_earning.keys():
            if user_earning.get(key)[0] <= final_points <= user_earning.get(key)[1]:
                level = key
                level_photo = user_earning_photos.get(key)
                break
        await call.message.answer_photo(caption=f"Поздравляю, тестик завершен!\n\nТы потенциально можешь получать <b>{level}</b>, неплохо, не так ли?",
                                        photo=level_photo)
        await call.message.answer_video_note(video_note=mentor_video_note)
        await asyncio.sleep(5)
        link = '<a href="https://t.me/slashstudy">Слеш</a>'
        await call.message.answer(f"Сорри за очередной кружок, но я не могу молчать)\n\n{link} - это твой старший брат в дизайне. Ментор, задача которого реально помочь тебе стать круче.")
        await asyncio.sleep(1.5)
        await call.message.answer("При этом не задолбать пушами и сухими ответами, а как настоящий друг: быть рядом, направлять на верный путь и поддерживать во время дороги")
        await asyncio.sleep(2)
        await call.message.answer('Сеньор и лид дизайнеры из Ozon, Yandex, СБЕР, МТС и других крупных компаний копнут в твои проблемы/хотелки и составят личный план развития в ноушене. По ходу пути все время будут с тобой отвечая на любые  вопросы, начиная от "Как создать компонент в фигме" заканчивая "Как забрать тендер с корпорацией"')
        await asyncio.sleep(2)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="🎁 Найти ментора", url="https://slashstudy.ru"))
        await call.message.answer(
            "Я считаю, будет честно подарить тебе скидку на первую встречу - 30% до начала лета. Залетай на сайт, она уже ждет тебя)",
            reply_markup=keyboard.as_markup())
        await state.clear()
        return
    elif last_question == 5:
        await call.message.delete()
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="🎁 Найти ментора", url="https://slashstudy.ru"))
        await call.message.answer(text=f"Половина вопросов позади, осталось еще чуть чуть. Мы хотим, чтобы ты становился лучше и придумали для тебя классно решение.\n\nПрокачивай свои скиллы в Слеш вместе с менторами из Ozon, Yandex, Сбер и других компаний, для этого забирай звонок с топом по скидке 25% до 20 апреля",reply_markup=keyboard.as_markup())
        await asyncio.sleep(2)
        next_keyboard = InlineKeyboardBuilder()
        next_keyboard.row(InlineKeyboardButton(text="Погнали дальше", callback_data="next_six_question"))
        await bot.send_video_note(chat_id=call.from_user.id, video_note=design_level_video_note2,
                                  reply_markup=next_keyboard.as_markup())
        return
    keyboard = InlineKeyboardBuilder()
    question = earnings_questions.get(f'{last_question + 1} вопрос')
    answers = list(question.get("answers").keys())
    random.shuffle(answers)
    for i, answer in enumerate(answers):
        keyboard.row(
            InlineKeyboardButton(text=options[i], callback_data=f"answer|{question.get('answers').get(answer)}|"
                                                                f"{last_question + 1}"))
    for i in range(len(answers)):
        answers[i] = f"{stickers[i]} {answers[i]}"
    text = (f"{last_question + 1}."
            f" {question.get('content')}") + "\n    " + "\n    ".join(answers)
    await call.message.edit_text(text=text)
    await call.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@earnings_level_router.callback_query(Text(text="next_six_question"), InputMessage.earning_level)
@is_subscriber
async def user_send_link(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.edit_reply_markup()
    keyboard = InlineKeyboardBuilder()
    last_question = 5
    question = earnings_questions.get(f'{last_question + 1} вопрос')
    answers = list(question.get("answers").keys())
    random.shuffle(answers)
    for i, answer in enumerate(answers):
        keyboard.row(
            InlineKeyboardButton(text=options[i], callback_data=f"answer|{question.get('answers').get(answer)}|"
                                                                f"{last_question + 1}"))
    for i in range(len(answers)):
        answers[i] = f"{stickers[i]} {answers[i]}"
    text = (f"{last_question + 1}."
            f" {question.get('content')}") + "\n    " + "\n    ".join(answers)
    await call.message.answer(text=text,
                              reply_markup=keyboard.as_markup())
