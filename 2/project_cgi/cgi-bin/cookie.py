#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import http.cookies
import os

# Отримуємо дані з форми
form = cgi.FieldStorage()

# Створюємо об'єкт cookies
cookie = http.cookies.SimpleCookie()

# Отримуємо значення cookies з запиту користувача
cookie.load(os.environ.get('HTTP_COOKIE', ''))

# Отримуємо поточне значення лічильника
count_cookie = cookie.get('form_counter')
count = int(count_cookie.value) if count_cookie else 0

# Перевірка, чи користувач натиснув кнопку "Видалити Cookies"
if 'delete_cookies' in form:
    # Видаляємо всі cookies
    cookie = http.cookies.SimpleCookie()
    count = 0  # Скидаємо лічильник
else:
    # Якщо користувач надіслав форму, збільшуємо лічильник
    if 'name' in form and 'email' in form:
        count += 1

# Оновлюємо cookies з новим лічильником
cookie['form_counter'] = count

# Встановлюємо час життя cookies (наприклад, 30 днів)
cookie['form_counter']['max-age'] = 30 * 24 * 60 * 60

# Виведення заголовка для cookies
print(cookie.output())
print("Content-type: text/html; charset=utf-8\n")

# HTML-код відповіді
html_response = """
<!DOCTYPE html>
<html>
<head>
    <title>Реалізація cookies</title>
</head>
<body>
    <h1>Реалізація cookies</h1>
    <p>Лічильник заповнених форм: {}</p>
    
    <form action="/cgi-bin/cookie.py" method="POST">
        <label for="name">Ім'я:</label>
        <input type="text" id="name" name="name"><br><br>
        
        <label for="email">Email:</label>
        <input type="text" id="email" name="email"><br><br>
        
        <input type="submit" value="Відправити форму">
    </form>
    
    <form action="/cgi-bin/cookie.py" method="POST">
        <input type="hidden" name="delete_cookies" value="true">
        <input type="submit" value="Видалити всі cookies">
    </form>
</body>
</html>
""".format(count)

print(html_response)
