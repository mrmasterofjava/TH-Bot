import time
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bs4 import BeautifulSoup
import schedule

# ⚡ Вставь сюда свой Telegram Token (полученный от BotFather)
TOKEN = "8124465634:AAGolfHNXTZyi11v8L0EUzXjt3uDx4Bq4ZY"
CHAT_ID = "1642610147"

# URL страницы "Твой ход"
URL = "https://tvoyhod.online/lk/surveys?tab=0"

# CSS-селектор для поиска опросов
SURVEY_SELECTOR = "div.SurveysTab_surveysPaper__zjFN6 div.MuiPaper-root.p-5"

# Инициализация Telegram бота
bot = Bot(token=TOKEN)
dp = Dispatcher()  # Инициализация Dispatcher без аргументов

# Храним последнее найденное название опроса
last_survey_title = None

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который будет уведомлять тебя о новых опросах на 'Твой ход'. Ожидай уведомлений!")

def check_surveys():
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
                bot.send_message(chat_id=CHAT_ID, text=f"🔔 Новый опрос на 'Твой ход'!\n\n{new_survey_title}\n\n👉 {URL}")
                print("✅ Отправлено уведомление о новом опросе!")
            else:
                bot.send_message(chat_id=CHAT_ID, text=f"Новых опросов пока нет'!")
                print("🔹 Новых опросов нет.")
        else:
            bot.send_message(chat_id=CHAT_ID, text=f"Новых опросов пока нет'!")
            print("❌ Не найден блок с опросами.")
    except Exception as e:
        print(f"⚠ Ошибка при проверке опросов: {e}")

# Запускаем проверку каждые 5 минут
schedule.every(5).minutes.do(check_surveys)

print("🚀 Бот запущен! Ждём новые опросы...")

if __name__ == '__main__':
    # Запуск бота
    dp.run_polling(bot, skip_updates=True)  # Используем run_polling вместо executor

    # Запуск планировщика
    while True:
        schedule.run_pending()
        time.sleep(60)