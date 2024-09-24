import requests

# Отправляем GET-запрос
response = requests.get('https://megamarket.ru/catalog/?q=macbook%20air%20m1&suggestionType=constructor')

# Проверяем статус запроса
if response.status_code == 200:
    print('Запрос выполнен успешно!')
    print(response.json())  # Выводим содержание страницы
else:
    print(f'Ошибка: {response.status_code}')
