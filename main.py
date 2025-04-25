import pytz
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime, time
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.CHAT_ID = os.getenv('CHAT_ID')
        self.TOPIC_ID = int(os.getenv('TOPIC_ID'))
        self.API_URL = os.getenv('API_URL')
        self.HEADERS = {
            "User-Agent": os.getenv("User-Agent"),
            "Accept": "application/json",
            "Authorization": os.getenv('Authorization')
        }

config = Config()

TELEGRAM_TOKEN = config.TELEGRAM_TOKEN
CHAT_ID = config.CHAT_ID
TOPIC_ID = config.TOPIC_ID
API_URL = config.API_URL
headers = config.HEADERS

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Функция для получения списка опросов
def get_surveys():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Возвращаем JSON с опросами
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None


# Функция для проверки новых опросов
async def check_surveys():
    surveys = get_surveys()['items']
    if surveys:
        message = (
            f"🔔 Новый опрос на 'Твой ход'!\n\n"
            f"Название: {surveys[0].get('name')}\n"
            f"Описание: {surveys[0].get('description')}\n"
            f"Ссылка: https://tvoyhod.online"
        )
        await bot.send_message(chat_id=CHAT_ID, message_thread_id=TOPIC_ID, text=message)
        print("✅ Отправлено уведомление о новом опросе!")
    else:
        await bot.send_message(chat_id=CHAT_ID, message_thread_id=TOPIC_ID, text="🔹 Новых опросов нет.")
        print("🔹 Новых опросов нет.")


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот, который будет уведомлять тебя о новых опросах на 'Твой ход'. Ожидай уведомлений!")


# Функция для запуска ежедневной проверки в 23:30 по московскому времени
async def daily_scheduler():
    moscow_tz = pytz.timezone("Europe/Moscow")  # Устанавливаем московское время
    while True:
        now = datetime.now(moscow_tz).time()  # Текущее время в Москве
        target_time = time(23, 30)  # Время 23:30

        if now.hour == target_time.hour and now.minute == target_time.minute:
            message = "🕒 Ежедневная проверка опросов на 'Твой ход'"
            await bot.send_message(chat_id=CHAT_ID, message_thread_id=TOPIC_ID, text=message)
            await check_surveys()
            await asyncio.sleep(60)  # Ждём минуту, чтобы не отправить сообщение несколько раз
        else:
            await asyncio.sleep(30)  # Проверяем время каждые 30 секунд


# Периодическая проверка опросов
async def periodic_scheduler():
    while True:
        await check_surveys()
        await asyncio.sleep(10800)  # Пауза 3 часа


# Запуск бота и планировщиков
async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        periodic_scheduler(),
        daily_scheduler()
    )


if __name__ == "__main__":
    asyncio.run(main())