import requests

# URL для получения списка опросов
API_URL = "https://tvoyhod.online/api/survey/list?"

# Ваш JWT-токен
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3Mzg3Njc3ODYsImV4cCI6MTc0Mzk1MTc4Niwicm9sZXMiOlsiUk9MRV9QVVBJTCJdLCJlbWFpbCI6Imlza2FuZGVyLm11c3RhZmluLjA1QG1haWwucnUifQ.cbxLytUCILm1x0j3pVSKtdv9nq18-Upi2gF4gp1FDizVLmicT5ACAonhRFS0D-R1r8YHljwLdn4gVjdIRe3b2H8TuOiysL7bj1akPEHwvLMILikOtzbADQ7k-evZWEhDJu2PS_8TBMd3LWtjefqUiN-Gvd90ZTrSa9f-lTBlDYIRKnYinpoAm6Ozk-D9dV9rAUeBJscY_WSI7q0jnKIA73Fr7W2G7uF7metPvbEBnNoaS6guds5gwTnjmwUiOmYm-nosWDhQXWGA7ZQapxk0Ls3UjqO2k5UjshGdXCw7tAdZSQMjVr_OfCJhdEifBAHAYCq086t0DDuP9alND_g9B_jlMuvkBubxjIftX1cMwZyOA_17D2TwE4iJf1jL0OnbqN7ZwxvV1vYcgqpYhYl6IWgtB3D-umJcBBtO3DY9HtFicNn_3XN7D6tHDE_Gk2szw5gyDBSvlWPgrL3MbHkTPsoYgwmD4qVEreMySaYX0yYXs2Z8ernqa84hMwnhDHFYYJcDuuRtKF2fYK2q2e-NdfIorc3a4azPvuOIkfAfKbpDucE8UglWE4Ft3cnXL5gVjWKy-juWb85Il8A-HqpoAh7i2qsKsXnDXsP6UIzB__T0Xomd1FbA4z5noYoec54vLaBXPvvrCO27zwFlsi4gIB2wzTnLCCmYWhan-XASiAc"

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"  # Добавляем токен
}

# Выполняем запрос к API
response = requests.get(API_URL, headers=headers)

# Проверяем ответ
survey = response.json()['items'][0]
if response.status_code == 200:
    print(survey)  # Вывод JSON
else:
    print(f"Ошибка {response.status_code}: {response.text}")