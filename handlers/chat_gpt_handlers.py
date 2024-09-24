import asyncio
import datetime
import io

from aiogram import Router, Bot, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.keyboards import keyboard_for_pay
from db.repository import operation_repository, users_repository, ai_requests_repository, ai_recommendations_repository
from settings import InputMessage
from utils.is_subscriber import is_subscriber
from utils.payment_for_services import create_payment, check_payment
from utils.rating_chat_gpt import RatingChatGpt

chat_gpt_router = Router()


@chat_gpt_router.callback_query(Text(startswith="ai_recommendation|"), any_state)
@chat_gpt_router.callback_query(Text(startswith="rofl_recommendation|"), any_state)
@is_subscriber
async def user_start_objective(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    delete_message_id = int(message.data.split("|")[1])
    await bot.delete_message(chat_id=message.from_user.id, message_id=delete_message_id)
    await message.message.answer("Привет! Этот бот создан ребятами из Слеш. Слеш — это твой старший брат в дизайне."
                                 " Мы помогаем войти в дизайн, а если ты уже тут, то гарантированно повысить"
                                 " ЗП или грейд.\n\nОбо всем написали в посте —> https://t.me/slashstudy/66")
    await asyncio.sleep(2)
    await message.message.answer("Спасибо! А теперь к боту")
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Начнем!", callback_data="start_objective"))
    await message.message.answer("<b>Небольшой дисклеймер</b>🔞\n\nЧтобы пользовать ботом, нужно отправить"
                                 " картинку. Мы не поддерживаем файлы и ссылки. Очень важно, что вещи связанные с"
                                 " политикой и конкретными личностями мы так же не обрабатываем.",
                                 reply_markup=keyboard.as_markup())


@chat_gpt_router.callback_query(Text(text="start_objective"), any_state)
@is_subscriber
async def start_attempts_bot(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    user = await users_repository.get_user_by_user_id(message.from_user.id)
    # if user.attempts > 0:
    await message.message.answer("Отправь мне картинку!")
    await state.set_state(InputMessage.objective_ai_recommendation_state)
    await state.update_data(delete_messege_id=message.message.message_id)
    # else:
    #     payment = await create_payment()
    #     await operation_repository.add_operation(operation_id=payment[0], user_id=message.from_user.id, is_paid=False,
    #                                              url=payment[1])
    #     keyboard = await keyboard_for_pay(payment_id=payment[0], url=payment[1])
    #     await message.message.answer('Для использования функции "Оценки дизайна через Ai" нужно приобрести паке'
    #                                  'т из 10 запросов за 250 рублей.\n\nПосле проведения платежи нажми на кнопку "Оплата произведена",'
    #                                      ' чтобы подтвердить платеж', reply_markup=keyboard.as_markup())
    await message.message.delete()


@chat_gpt_router.callback_query(Text(startswith="is_paid|"), any_state)
@is_subscriber
async def pay_attempts_bot(message: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = message.data.split("|")
    payment_id = data[1]
    user = await users_repository.get_user_by_user_id(message.from_user.id)
    if await check_payment(payment_id):
        await operation_repository.update_paid_by_operation_id(payment_id)
        await users_repository.give_attempts_by_user_id(user_id=message.from_user.id, attempts=10)
        await state.set_state(InputMessage.objective_ai_recommendation_state)
        if not user.donate:
            await users_repository.update_donate_by_user_id(user_id=message.from_user.id)
        my_message = await message.message.edit_text("Все круто! Мы получили оплату и теперь тебе доступны 10 запросов"
                                                        " к нашему Ai сервису.\n\nПросто отправь картинку и получи рекомендации")
        await state.update_data(delete_messege_id=my_message.message_id)
        try:
            keyboard = InlineKeyboardBuilder()
            keyboard.row(InlineKeyboardButton(text="В меню", callback_data="start_menu"))
            await message.message.edit_reply_markup(reply_markup=keyboard.as_markup())
        finally:
            return
    else:
        try:
            payment = await operation_repository.get_operation_by_operation_id(payment_id)
            keyboard = await keyboard_for_pay(payment_id=payment_id, url=payment.url)
            await message.message.edit_text("Пока мы не видим, чтобы оплата была произведена( Погоди"
                                            " еще немного времени и убедись,"
                                            " что ты действительно произвел оплату. Если что-то пошло не так, свяжись"
                                            " с нами с помощью команды /contact_us в нашем боте",
                                            reply_markup=keyboard.as_markup())
        finally:
            return


@chat_gpt_router.message(F.photo, InputMessage.objective_ai_recommendation_state)
@is_subscriber
async def get_photo_objective(message: types.Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    delete_message_id = state_data.get("delete_message_id")
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=delete_message_id)
    except:
        print("Not_delete")
    user = await users_repository.get_user_by_user_id(message.from_user.id)
    # if user.attempts <= 0:
    #     payment = await create_payment()
    #     await operation_repository.add_operation(operation_id=payment[0], user_id=message.from_user.id, is_paid=False,
    #                                              url=payment[1])
    #     keyboard = await keyboard_for_pay(payment_id=payment[0], url=payment[1])
    #     await message.answer('Для использования функции "Оценки дизайна через Ai" нужно приобрести паке'
    #                                  'т из 10 запросов за 250 рублей.\n\nПосле проведения платежа нажми на кнопку "Оплата произведена",'
    #                                  ' чтобы подтвердить платеж', reply_markup=keyboard.as_markup())
    #     return
    delete_message = await message.answer("Приняли твой дизайн 🎨. Нужно немного времени ⏳, чтобы проанализировать"
                                          " и дать ответ.")
    photo_bytes_io = io.BytesIO()
    photo_id = message.photo[-1].file_id
    await bot.download(message.photo[-1], destination=photo_bytes_io)
    text = await RatingChatGpt(photo_bytes_io).assessment(True)
    if 'правьте другую картинку' in text:
        await ai_requests_repository.add_request(photo_id=photo_id, user_id=message.from_user.id, answer_ai=text)
        await bot.delete_message(message_id=delete_message.message_id, chat_id=message.from_user.id)
        await message.answer("Извини, но эта фотография не поддерживается! Пришли другую (Количество твоих попыток не уменьшилось)")
        await message.delete()
        return
    else:
        await ai_requests_repository.add_request(photo_id=photo_id, user_id=message.from_user.id, answer_ai=text)
        await message.answer(text=text)
        await bot.delete_message(message_id=delete_message.message_id, chat_id=message.from_user.id)
        await asyncio.sleep(2)
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="В меню", callback_data="start_menu"))
        await users_repository.delete_attempt_by_user_id(user_id=message.from_user.id)
        if user.donate:
            await message.answer("Отлично! Хочешь еще больше улучшений? Просто отправь еще одну картинку 📸, и наша"
                                 f" Ai модель подскажет, что можно сделать лучше.")
                                 # f" \n\nУ тебя осталось еще {user.attempts - 1} запросов", reply_markup=keyboard.as_markup())
        else:
            await message.answer("Отлично! Хочешь еще больше улучшений? Просто отправь еще одну картинку 📸, и наша"
                                 f" Ai модель подскажет, что можно сделать лучше",
                                 reply_markup=keyboard.as_markup())
        user = await ai_recommendations_repository.get_user_by_user_id(user_id=message.from_user.id)
        if user is None:
            await ai_recommendations_repository.add_ai_recommendation(user_id=message.from_user.id,
                                                                      last_date_start=datetime.datetime.now())
        else:
            await ai_recommendations_repository.update_user_last_start_date_by_user_id(user_id=message.from_user.id)

