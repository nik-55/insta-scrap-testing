# This file contain api for testing bot only and will be removed after proper flask setup 

from flask import Flask
from bot.insta_bot.scrape_posts import ScrapePost
from database.db import create_tables, save_posts, read_posts, does_club_exist

app = Flask(__name__)

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

if __name__ == '__main__':
    create_tables()
    app.run()