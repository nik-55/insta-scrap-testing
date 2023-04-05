# This file contain api for testing bot only and will be removed after proper flask setup 

from flask import Flask, request
from bot.insta_bot.scrape_posts import ScrapePost
from database.db import create_tables, save_posts, read_posts, does_club_exist, save_user,add_club,login_required
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'
from views.auth import auth
app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(auth)

@app.route('/posts/<username>')
def getPosts(username):
    try:
        if does_club_exist(username):
            print("Club exist so no need to scrape...")
            return read_posts(username)
        else:
            print("Scraping....")
            posts = ScrapePost().getPosts(username)
            save_posts(posts,username)
            return posts
    except Exception as error:
        print(error)
        return "error"
    
@app.route('/users/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return save_user(username,password)

@app.route('/users/addclub')
@login_required
def addclub():
    return add_club()

if __name__ == '__main__':
    create_tables()
    app.run()