# This file contain api for testing bot only and will be removed after proper flask setup

from flask import Flask

app = Flask(__name__)

@app.route('/posts/<username>')
def getPosts(username):
    return username

if __name__ == '__main__':
    app.run()