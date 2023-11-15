from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b"secret"

app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from application import views