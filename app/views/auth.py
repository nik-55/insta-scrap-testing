from flask import Blueprint, request, session
from database.db import save_user
from models.user import User
from functools import wraps
from hashlib import md5

auth = Blueprint("auth", __name__)


def hash_password(password):
    try:
        pwd = md5((password).encode("utf-8")).hexdigest()
        return pwd
    except:
        raise Exception("error in hashing")


def set_session(user):
    try:
        session["logged_in"] = True
        session["user_id"] = user.id
    except Exception as error:
        raise Exception("error occur in setting session")


def get_user_from_session():
    try:
        if session and session.get("logged_in"):
            user = User.get(User.id == session.get("user_id"))
            if user:
                return user
        raise Exception("Invalid Session")
    except Exception as error:
        raise Exception("Error occur in getting user from session")


def validate_user(username, password):
    try:
        user = User.get(User.username == username)
        if user and user.password == password:
            return user
        raise Exception("user not found")
    except Exception as error:
        raise ("Error occured in authenticating user")


def authenticate(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            user = get_user_from_session()
            if not user:
                raise Exception("Unauthorized access")
            request.user = user
            return f(*args, **kwargs)
        except Exception as error:
            return "Unauthorized error"

    return inner


@auth.route("/users/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        pwd = hash_password(password=password)
        return save_user(username, password=pwd)
    except Exception as error:
        return "Not registered"


@auth.route("/users/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        pwd = hash_password(password=password)
        user = validate_user(username, pwd)
        if user:
            set_session(user=user)
            return "Logged in successfully"
        raise Exception("user not exist")
    except Exception as error:
        return "error occur while logging in"


@auth.route("/users/logout", methods=["GET"])
@authenticate
def logout():
    try:
        session.pop("user_id", None)
        return "logout"
    except Exception as error:
        return "error in loging out"
