# This file contain api for testing bot only and will be removed after proper flask setup 

from flask import Flask
from database.db import create_tables
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'
from views.auth import auth
from views.posts import posts, scrape_posts

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=["GET"])
def _():
    return "Club noticeboard backend"

app.register_blueprint(auth)
app.register_blueprint(posts)

if __name__ == '__main__':
    create_tables()
    # scrape_posts()
    app.run()