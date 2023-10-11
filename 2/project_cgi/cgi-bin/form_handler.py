#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi

print("Content-type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
programming_language = form.getvalue("programming_language")
hobbies = form.getlist("hobbies")

html_response = """
<!DOCTYPE html>
<html>
<head>
    <title>Результат вибору</title>
</head>
<body>
    <h1>Результат вашого вибору</h1>
    <p>Ваше ім'я: {}</p>
    <p>Email: {}</p>
    <p>Стать: {}</p>
    <p>Обрана мова програмування: {}</p>
    <p>Хобі:</p>
    <ul>
""".format(name, email, gender, programming_language)

for hobby in hobbies:
    html_response += "<li>{}</li>\n".format(hobby)

html_response += """
    </ul>
</body>
</html>
"""

print(html_response)
