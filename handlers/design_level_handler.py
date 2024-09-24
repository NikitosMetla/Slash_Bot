import asyncio
import datetime
import random

from aiogram import Router, Bot, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.keyboards import start_keyboard, menu_keyboard
from db.repository import users_repository, design_level_repository, admin_repository
from settings import design_questions, InputMessage, user_levels, options, stickers, start_photo_id, \
    design_level_photo_id, level_photos, design_level_video_note2, mentor_video_note
from utils.is_subscriber import is_subscriber

design_level_router = Router()


@design_level_router.message(Text(text="/contact_us"), any_state)
@is_subscriber
async def contact_us(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    if not await users_repository.get_user_by_user_id(message.from_user.id):
        await users_repository.add_user(user_id=message.from_user.id, username=message.from_user.username, attempts=3,
                                        donate=False)
    message = await message.answer(text="Напиши нам волнующий тебя вопрос! Это может быть как пожелания по улучшению"
                                        " бота, так и просьба о помощи с работой с ботом",
                                   reply_markup=menu_keyboard.as_markup())
    await state.set_state(InputMessage.contact_us_state)
    await state.update_data(message_id=message.message_id)


@design_level_router.message(F.text, InputMessage.contact_us_state)
@is_subscriber
async def send_user_question(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")
    await message.answer(text="Твой вопрос в скором времени просмотрит администратор"
                              " и постарается как можно раньше тебе ответить!", reply_markup=menu_keyboard.as_markup())
    await bot.delete_message(message_id=message_id, chat_id=message.from_user.id)
    admins = await admin_repository.select_all_admins()
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Ответить пользователю",
                                      callback_data=f"answer_user|{message.from_user.id}|{message.from_user.username}"))
    for admin in admins:
        try:
            from bot_admin import admin_bot
            await admin_bot.send_message(text=f"Вопрос от пользователя с id: {message.from_user.id},"
                                         f" username: @{message.from_user.username}\n\n<i>{message.text}</i>",
                                         chat_id=admin.admin_id,
                                         reply_markup=keyboard.as_markup())
        except:
            continue
    await state.clear()


@design_level_router.callback_query(Text(text="start_menu_delete"), any_state)
@design_level_router.callback_query(Text(text="start_menu"), any_state)
@design_level_router.message(Text(text="/start"), any_state)
@is_subscriber
async def start(message: types.Message | types.CallbackQuery, state: FSMContext, bot: Bot):
    if not await users_repository.get_user_by_user_id(message.from_user.id):
        await users_repository.add_user(user_id=message.from_user.id, username=message.from_user.username, attempts=3,
                                        donate=False)
    if type(message) == types.CallbackQuery:
        next_message = await message.message.answer_photo(start_photo_id, "Выбирай, чего желаешь: узнать свою ЗП по рынку, крутануть"
                                                                          " рулетку на определения скиллов"
                                                                          " в дизайне, забрать самую большую базу по дизайну"
                                                                          " или получить личного ментора из топовой"
                                                                          " компании!")
        if message.data != 'start_menu_delete':
            await message.message.delete()
    else:
        next_message = await message.answer_photo(start_photo_id, "Выбирай, чего желаешь: узнать свою ЗП по рынку, крутануть"
                                                                          " рулетку на определения скиллов"
                                                                          " в дизайне, забрать самую большую базу по дизайну"
                                                                          " или получить личного ментора из топовой"
                                                                          " компании!")
    await next_message.edit_reply_markup(reply_markup=start_keyboard(next_message.message_id).as_markup())
    await state.clear()


@design_level_router.callback_query(Text(startswith="start_design_level|"), any_state)
@is_subscriber
async def user_send_link(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    delete_message_id = int(message.data.split("|")[1])
    keyboard = InlineKeyboardBuilder()
    # user = Users(message.from_user.id, "design_level")
    user = await design_level_repository.get_user_by_user_id(user_id=int(message.from_user.id))
    if user is None:
        await design_level_repository.add_design_level(user_id=message.from_user.id, finish_service=False,
                                                       last_date_start=datetime.datetime.now())
    else:
        await design_level_repository.update_user_last_start_date_by_user_id(user_id=int(message.from_user.id))
        if user.finish_service:
            await design_level_repository.update_finish_service_by_user_id(user_id=int(message.from_user.id))

    # await user.read_data()
    # await user.add_user()
    question = design_questions.get('1 вопрос')
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
    await message.message.answer_photo(caption="Стартуем тест <b>«Кто ты по дизайну?»</b>! Тебя ждут"
                                               " десять вопросов и ответ, кто ТЫ из лысых котов",
                                       photo=design_level_photo_id)
    await asyncio.sleep(2)
    await message.message.answer(text=text, reply_markup=keyboard.as_markup())
    await state.set_state(InputMessage.design_level)
    await state.update_data(last_question=1)


@design_level_router.callback_query(Text(startswith="answer|"), InputMessage.design_level)
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
        await design_level_repository.update_finish_service_by_user_id(user_id=int(call.from_user.id))
        # await user.read_data()
        # await user.edit_completion()
        final_points = sum(points.values()) - int(points.get("last_question"))
        level = ""
        level_photo = ""
        for key in user_levels.keys():
            if user_levels.get(key)[0] <= final_points <= user_levels.get(key)[1]:
                level = key
                level_photo = level_photos.get(key)
                break
        delete_message = await call.message.answer("Поздравляю, тестик завершен!   Я вижу твоим грейдом...")
        await asyncio.sleep(2)
        await delete_message.delete()
        await call.message.answer_photo(caption=f"Загрузочка прошла, твой грейд -> ({level})",
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
        await call.message.answer("Я считаю, будет честно подарить тебе скидку на первую встречу - 30% до начала лета. Залетай на сайт, она уже ждет тебя)",
                                  reply_markup=keyboard.as_markup())
        await state.clear()
        return
    elif last_question == 5:
        await call.message.delete()
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="🎁 Найти ментора", url="https://slashstudy.ru"))
        await call.message.answer(text=f"Половина вопросов позади, осталось еще чуть чуть. Мы хотим, чтобы ты становился лучше и придумали для тебя классно решение.\n\nПрокачивай свои скиллы в Слеш вместе с менторами из Ozon, Yandex, Сбер и других компаний, для этого забирай звонок с топом по скидке 25% до 20 апреля", reply_markup=keyboard.as_markup())
        await asyncio.sleep(2)
        next_keyboard = InlineKeyboardBuilder()
        next_keyboard.row(InlineKeyboardButton(text="Погнали дальше", callback_data="next_six_question"))
        await bot.send_video_note(chat_id=call.from_user.id, video_note=design_level_video_note2, reply_markup=next_keyboard.as_markup())
        return
    keyboard = InlineKeyboardBuilder()
    question = design_questions.get(f'{last_question + 1} вопрос')
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


@design_level_router.callback_query(Text(text="next_six_question"), InputMessage.design_level)
@is_subscriber
async def user_send_link(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.edit_reply_markup()
    keyboard = InlineKeyboardBuilder()
    last_question = 5
    question = design_questions.get(f'{last_question + 1} вопрос')
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
    await call.message.answer(text=text, reply_markup=keyboard.as_markup())