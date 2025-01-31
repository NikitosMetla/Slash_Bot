# 🎨 Telegram Бот для Оценки Дизайна и Грейда ЗП – "Слеш Дизайн"

## 📌 Описание проекта

Данный Telegram-бот предназначен для дизайнеров, желающих определить свой профессиональный уровень, узнать предполагаемый грейд заработной платы и получить экспертную оценку своих работ. Бот также предоставляет доступ к базе знаний студии "Слеш".

## 🚀 Функциональные возможности

- 📊 **Оценка уровня дизайнера** – определение грейда и зарплатного диапазона.
- 🖼 **Анализ дизайна** – загрузка работы для получения оценки от AI (ChatGPT).
- 📚 **База знаний** – доступ к материалам и статьям студии "Слеш".
- 🔑 **Подписка на продвинутый анализ** – расширенный функционал анализа дизайна через платную подписку (YooKassa).

## 🌐 Запуск проекта

### 1. Склонируйте репозиторий
```bash
git clone https://github.com/NikitosMetla/Slash_Design_Bot.git
cd Slash_Design_Bot
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Запуск бота
```bash
python main_bot.py
```

## 🔧 Переменные окружения (`.env`)

```ini
MAIN_BOT_TOKEN=your_telegram_bot_token
ADMIN_BOT_TOKEN=your_admin_bot_token
SHOP_ID=your_shop_id
SECRET_KEY=your_secret_key
GPT_TOKEN=your_openai_api_key
POSTGRES_DB=design_db
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_PORT=5432
POSTGRES_HOST=db_host
```

## 💪 Используемые технологии
- **Python 3.11**
- **Aiogram 3.0.0b7**
- **PostgreSQL + SQLAlchemy**
- **Requests**
- **YooKassa API**

## 🎲 `requirements.txt`
```ini
SQLAlchemy==2.0.30
python-dotenv==1.0.0
aiogram==3.0.0b7
requests==2.32.3
yookassa==3.1.0
```

## 💬 Обратная связь

📧 Email: your-email@example.com  
👉 Telegram: [@yourusername](https://t.me/yourusername)  
📚 GitHub: [NikitosMetla](https://github.com/NikitosMetla)  

