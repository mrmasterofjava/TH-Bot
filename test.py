import requests
import urllib.parse
import json

# URL для аутентификации
AUTH_URL = "https://tvoyhod.online/auth/signin"

# URL для получения списка опросов
API_URL = "https://tvoyhod.online/api/survey/list?"

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0",
    "Accept": "application/json"
}

# Данные для аутентификации
auth_data = {
    "email": "iskander.mustafin.05@mail.ru",  # Замените на ваш email
    "password": "TheFlash01"         # Замените на ваш пароль
}


def authenticate(auth_url, auth_data, headers):
    """
    Выполняет аутентификацию и возвращает токен (если успешно) или None.
    """
    try:
        # Попробуйте GET запрос с параметрами
        auth_response = requests.get(auth_url, params=auth_data, headers=headers)

        print(f"Аутентификация - Статус код: {auth_response.status_code}")
        print(f"Аутентификация - Content-Type: {auth_response.headers.get('Content-Type')}")
        print(f"Аутентификация - Содержимое ответа: {auth_response.text}")

        if auth_response.status_code == 200:
            try:
                # Попробуйте распарсить JSON
                json_data = auth_response.json()
                token = json_data.get("token")

                if token:
                    print(f"Аутентификация - Токен получен: {token}")
                    return token
                else:
                    print("Аутентификация - Токен не найден в JSON.")
                    return None

            except json.JSONDecodeError as e:
                print(f"Аутентификация - Ошибка JSON: {e}")
                return None

        else:
            print(f"Аутентификация - Ошибка: {auth_response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Аутентификация - Ошибка подключения: {e}")
        return None


def get_survey_list(api_url, headers):
    """
    Получает список опросов, используя переданный токен в заголовках.
    """
    try:
        response = requests.get(api_url, headers=headers)

        print(f"Список опросов - Статус код: {response.status_code}")
        print(f"Список опросов - Content-Type: {response.headers.get('Content-Type')}")
        print(f"Список опросов - Содержимое ответа: {response.text}")

        if response.status_code == 200:
            try:
                survey_list = response.json()
                print("Список опросов - JSON получен:")
                print(survey_list)
                return survey_list
            except json.JSONDecodeError as e:
                print(f"Список опросов - Ошибка JSON: {e}")
                return None
        else:
            print(f"Список опросов - Ошибка: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Список опросов - Ошибка подключения: {e}")
        return None

# --- Основной код ---
token = authenticate(AUTH_URL, auth_data, headers)

if token:
    headers["Authorization"] = f"Bearer {token}"
    get_survey_list(API_URL, headers)
else:
    print("Не удалось получить токен.  Завершение работы.")
