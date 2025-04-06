import pytz
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime, time


# Telegram Token (полученный от BotFather)
TELEGRAM_TOKEN = "8124465634:AAEeUqb8_ArkwysviD4ZIuCfjsCKN8FZPrk"
CHAT_ID = "-1002181671988"  # ID чата, куда бот будет отправлять уведомления
TOPIC_ID = 781


# URL для получения списка опросов
API_URL = "https://tvoyhod.online/api/survey/list?"

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3Mzk5NTUzODIsImV4cCI6MTc0NTEzOTM4Miwicm9sZXMiOlsiUk9MRV9QVVBJTCJdLCJlbWFpbCI6Imlza2FuZGVyLm11c3RhZmluLjA1QG1haWwucnUifQ.MA-ddkfMtHKU0BUaxN0OzpQVLF--m1aHq8h-i5gAvk3DXIMzjyO0wvI2aE1ayjTeEpyqEdO77YmAKBUBcN_BXTVtcKK2J7G_1VvE5cF0DHR11k0ge6-7OWbq39nXpj5prnk8jv7342Bb9rjxNXliLmWxmG4SXc1lCt5Psmjkm-ReHKEovNYTUcimJvA1kM-xmptFyt8AAZZ06_B91Hpnh1pGbJ75gUFZ0zLxbwoILSDMgsPSbljqxizGpts2vMZKwQ06x-lRIxMTcHJ-TwpykpTiqraCpzIccQQmbebqBQoxLsDMnqcq_364oNwa8WC31qH8w27-G3IUFNDGMS402w1trk51oWfOcKslcvOXDdbxic2DPM7QaI9ZEfcVK93gF7AuyUV5vVfC-h1ybDxu9rWC2510APUVAQzgNfWAC9CUpRoCSuSqCRg21Ps-kjCw2NkIE4pVGkktlGCQoky5SDu8liwPEXcgyJoE_WY7aZ7PHe8PvhCREyYC53C40_l0cZjrFB5zn75PPB9JhTzqq6_hKeppq-PLCw4naU94KUC6YL0FDUQ4hxwJN4f0PZC-EKRjjOjF2sKgXVacUe3ln5N2hqSCj7eNMBxQtxrabgycK8Cc_0wypxq9stYBsiuEGAfiwPxCRJ7DEX_Ks7e42kLMk4BCWM-sMlX8fmspFdY"
}

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()



# Функция для получения списка опросов
def get_surveys():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json() # Возвращаем JSON с опросами
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
        await bot.send_message(chat_id=CHAT_ID,message_thread_id=TOPIC_ID, text=message)
        print("✅ Отправлено уведомление о новом опросе!")
    else:
        await bot.send_message(chat_id=CHAT_ID, message_thread_id=TOPIC_ID,text="🔹 Новых опросов нет.")
        print("🔹 Новых опросов нет.")


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который будет уведомлять тебя о новых опросах на 'Твой ход'. Ожидай уведомлений!")


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
