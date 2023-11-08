import json
from os import path

def _get_credentials_filepath(filename="credentials.json"):
    parent_dir = path.abspath( path.dirname(__file__) )
    filepath = path.join(parent_dir, filename)
    return filepath

_filepath = _get_credentials_filepath()

def _load_credentials():
    with open(_filepath, "r", encoding="utf-8") as file:
        json_obj = json.load(file)

    return json_obj

def _dump_credentials(json_obj):
    with open(_filepath, "w", encoding="utf-8") as file:
        json.dump(json_obj, file)

user_credentials = _load_credentials()

def get_user_credentials(username):
    for user in user_credentials:
        if user["username"] == username:
            return user
    return None

def change_user_password(user, new_password):
    try:
        user["password"] = new_password
        _dump_credentials(user_credentials)
    except Exception as e:
        return 1
    return 0
