from flask import Blueprint, request

auth = Blueprint(name='auth',import_name= __name__, url_prefix='/auth')

@auth.post("/register")
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

@auth.post("/login")
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']