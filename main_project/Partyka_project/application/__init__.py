from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
basic_auth = HTTPBasicAuth(scheme='Bearer')

def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)

    JWTManager(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    with app.app_context():
        from .portfolio import portfolio_blueprint
        from .auth import auth_blueprint
        from .info import info_blueprint
        from .todo import todo_blueprint
        from .users import users_blueprint
        from .post import post_blueprint
        from .api import api_bp
        from .auth_api import auth_api_bp

        app.register_blueprint(portfolio_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(info_blueprint)
        app.register_blueprint(todo_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(post_blueprint)
        app.register_blueprint(api_bp)
        app.register_blueprint(auth_api_bp)
    
    return app