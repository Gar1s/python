from flask import Flask, render_template, request
import os
from datetime import datetime
from flask import request

app = Flask(__name__)

my_skills = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Flask'},
    {'id': 3, 'name': 'HTML'},
    {'id': 4, 'name': 'CSS'},
]

@app.route('/')
def home():    
    return render_template('base.html', title='Головна сторінка', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/page1')
def page1():
    return render_template('page1.html', title='Сторінка 1', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/page2')
def page2():
    return render_template('page2.html', title='Сторінка 2', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/page3')
def page3():
    return render_template('page3.html', title='Сторінка 3', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    if id:
        skill = next((skill for skill in my_skills if skill['id'] == id), None)
        if skill:
            return f"Навичка: {skill['name']}"
        return 'Навичка не знайдена'
    else:
        skills_list = ', '.join(skill['name'] for skill in my_skills)
        return f"Усі навички: {skills_list} (Загальна кількість: {len(my_skills)})"


if __name__ == '__main__':
    app.run(debug=True)
