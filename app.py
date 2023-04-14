# This file contain api for testing bot only and will be removed after proper flask setup 

from flask import Flask
from app.database.db import create_tables
from app.views.auth import auth
from app.views.posts import posts, scrape_posts
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

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