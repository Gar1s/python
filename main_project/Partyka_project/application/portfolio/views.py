from datetime import datetime
import platform
from flask import request, render_template

from . import portfolio_blueprint

os_info = platform.system()
current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

my_skills = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Flask'},
    {'id': 3, 'name': 'HTML'},
    {'id': 4, 'name': 'CSS'},
]

@portfolio_blueprint.route('/')
def home():
    user_agent=request.user_agent    
    return render_template('home.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@portfolio_blueprint.route('/page1')
def page1():
    return render_template('page1.html', title='About Me', os_info=os_info, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@portfolio_blueprint.route('/skills')
def skills():
    return render_template('skills.html', my_skills=my_skills)