import pytz
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime, time


# Telegram Token (полученный от BotFather)
TELEGRAM_TOKEN = "8124465634:AAGolfHNXTZyi11v8L0EUzXjt3uDx4Bq4ZY"
CHAT_ID = "-1002181671988"  # ID чата, куда бот будет отправлять уведомления
TOPIC_ID = 781


# URL для получения списка опросов
API_URL = "https://tvoyhod.online/api/survey/list?"

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0",
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3Mzg3Njc3ODYsImV4cCI6MTc0Mzk1MTc4Niwicm9sZXMiOlsiUk9MRV9QVVBJTCJdLCJlbWFpbCI6Imlza2FuZGVyLm11c3RhZmluLjA1QG1haWwucnUifQ.cbxLytUCILm1x0j3pVSKtdv9nq18-Upi2gF4gp1FDizVLmicT5ACAonhRFS0D-R1r8YHljwLdn4gVjdIRe3b2H8TuOiysL7bj1akPEHwvLMILikOtzbADQ7k-evZWEhDJu2PS_8TBMd3LWtjefqUiN-Gvd90ZTrSa9f-lTBlDYIRKnYinpoAm6Ozk-D9dV9rAUeBJscY_WSI7q0jnKIA73Fr7W2G7uF7metPvbEBnNoaS6guds5gwTnjmwUiOmYm-nosWDhQXWGA7ZQapxk0Ls3UjqO2k5UjshGdXCw7tAdZSQMjVr_OfCJhdEifBAHAYCq086t0DDuP9alND_g9B_jlMuvkBubxjIftX1cMwZyOA_17D2TwE4iJf1jL0OnbqN7ZwxvV1vYcgqpYhYl6IWgtB3D-umJcBBtO3DY9HtFicNn_3XN7D6tHDE_Gk2szw5gyDBSvlWPgrL3MbHkTPsoYgwmD4qVEreMySaYX0yYXs2Z8ernqa84hMwnhDHFYYJcDuuRtKF2fYK2q2e-NdfIorc3a4azPvuOIkfAfKbpDucE8UglWE4Ft3cnXL5gVjWKy-juWb85Il8A-HqpoAh7i2qsKsXnDXsP6UIzB__T0Xomd1FbA4z5noYoec54vLaBXPvvrCO27zwFlsi4gIB2wzTnLCCmYWhan-XASiAc"
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
