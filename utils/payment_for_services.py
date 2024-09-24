from os import getenv

from dotenv import load_dotenv, find_dotenv
from yookassa import Configuration, Payment


load_dotenv(find_dotenv("../.env"))
Configuration.account_id = getenv("SHOP_ID")
Configuration.secret_key = getenv("SECRET_KEY")


async def create_payment(amount: int = 250,
                         currency: str = "RUB",
                         description: str = "Оплата ai рекомендаций",
                         return_url: str = "https://t.me/slashstudy_bot"):
    # Создаем платеж
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": currency
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": description
    })

    return payment.id, payment.confirmation.confirmation_url


async def check_payment(payment_id):
    payment = Payment.find_one(payment_id)
    return payment.status == 'succeeded'