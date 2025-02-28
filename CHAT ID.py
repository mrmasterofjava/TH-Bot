import requests

# Вставьте сюда токен вашего бота
TOKEN = "8124465634:AAGolfHNXTZyi11v8L0EUzXjt3uDx4Bq4ZY"

# Очистка обновлений
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=0"
response = requests.get(url)

# Получение новых обновлений
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
response = requests.get(url)

# Проверяем ответ
if response.status_code == 200:
    data = response.json()
    if data["result"]:
        for update in data["result"]:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "Нет текста")
                print(f"ID чата: {chat_id}, Сообщение: {text}")
                print(response.json())
    else:
        print("Нет новых обновлений. Отправьте боту сообщение.")
else:
    print(f"Ошибка: {response.status_code}, {response.text}")