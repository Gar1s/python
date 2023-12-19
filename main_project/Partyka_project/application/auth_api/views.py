from datetime import datetime, timedelta
from flask import jsonify, request
import jwt

from application.auth.models import User
from config import Config
from . import auth_api_bp
from application import basic_auth

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return username

@basic_auth.error_handler
def auth_error(status):
    return jsonify(message = "Wrong data! Access denied!") , status

def generate_token(username, token_type, expiry):
    token = jwt.encode(
        {"sub": token_type, "username": username, "exp": expiry},
        Config.SECRET_KEY, 
        algorithm="HS256"
    )
    return token

@auth_api_bp.route('/login')
def login():
    auth = request.authorization

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return {
            "message": "Wrong credentials"
        }, 401
         
    if user.verify_password(auth.password):
        access_expiry = datetime.utcnow() + timedelta(minutes=30)
        access_token = generate_token(user.username, "access", access_expiry)

        return jsonify(
            {
                "access_token": access_token,
            }
        )
    
    return {
            "message": "Wrong credentials"
        }, 401