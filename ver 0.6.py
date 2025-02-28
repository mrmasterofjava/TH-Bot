import time
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bs4 import BeautifulSoup
import schedule
import asyncio

# ⚡ Вставь сюда свой Telegram Token (полученный от BotFather)
TOKEN = "8124465634:AAGolfHNXTZyi11v8L0EUzXjt3uDx4Bq4ZY"
CHAT_ID = "1642610147"

# URL страницы "Твой ход"
URL = "https://tvoyhod.online/lk/surveys?tab=0"

# CSS-селектор для поиска опросов
SURVEY_SELECTOR = "div.SurveysTab_surveysList__onetw h2"

# Инициализация Telegram бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним последнее найденное название опроса
last_survey_title = None

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который будет уведомлять тебя о новых опросах на 'Твой ход'. Ожидай уведомлений!")

async def check_surveys():
    global last_survey_title

    try:
        # Запрос к сайту
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Ищем блок с опросами
        survey_block = soup.select_one(SURVEY_SELECTOR)

        if survey_block:
            # Получаем текст первого опроса (если есть)
            new_survey_title = survey_block.get_text(strip=True)

            # Если это новый опрос — отправляем уведомление
            if new_survey_title != last_survey_title:
                last_survey_title = new_survey_title
                await bot.send_message(chat_id=CHAT_ID, text=f"🔔 Новый опрос на 'Твой ход'!\n\n{new_survey_title}\n\n👉 {URL}")
                print("✅ Отправлено уведомление о новом опросе!")
            else:
                await bot.send_message(chat_id=CHAT_ID, text=f"Новых опросов пока нет'!")
                print("🔹 Новых опросов нет.")
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f"Не найден блок с опросами'!")
            print("❌ Не найден блок с опросами.")
    except Exception as e:
        print(f"⚠ Ошибка при проверке опросов: {e}")

# Запускаем проверку каждые 5 минут
async def scheduler():
    while True:
        await check_surveys()
        await asyncio.sleep(300)  # Пауза 5 минут

print("🚀 Бот запущен! Ждём новые опросы...")


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        scheduler()
    )

if __name__ == "__main__":
    asyncio.run(main())