from .config import database
from models.post import Post
from models.club import Club
from models.user import User
from models.user_club_relationship import Relationship
from flask import session,redirect,url_for
from functools import wraps
from hashlib import md5

def create_tables():
    with database:
        database.create_tables([Post,Club,User,Relationship])

def save_posts(posts,username):
    club = Club.create(username=username)
    with database.atomic():
        for post in posts:
            Post.create(src=post['src'],caption=post['caption'],club=club)

def does_club_exist(username):
    query = Club.select().where(Club.username==username)
    if len(query)>0:
        return True
    return False

def read_posts(username):
    try:
        query = Club.select().where(Club.username==username)
        posts = []
        for temp in query:
            for post in temp.posts:
                posts.append({'id':post.id,'caption':post.caption,'src':post.src})
        return posts
    except Exception as error:
        print(error)
        return "error"


def add_club():
    club = Club.select().where(Club.username == "mdgspace")
    user = User.select().where(User.username== get_current_user())
    Relationship.create(user=user,club=club)
    return "added successfully"

def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username

def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])
    
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner

def save_user(username,password):
    pwd = md5((password).encode('utf-8')).hexdigest(),
    user = User.create(username=username,password=pwd) 
    auth_user(user)
    return "Register successfully"