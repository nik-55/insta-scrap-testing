from .auth import authenticate
from flask import Blueprint, request
from app.models.club import Club
from app.models.club_user_relationship import ClubUserRelationship
from app.bot.insta_bot.scrape_posts import ScrapePost
from app.database.db import save_posts, subscribe_club
import threading

posts = Blueprint("posts", __name__)


@posts.route("/club/posts/<username>", methods=["GET"])
@authenticate
def getPosts(username):
    try:
        club = Club.get(Club.username == username)
        posts = []
        for post in club.posts:
            posts.append({"id": post.id, "caption": post.caption, "src": post.src})
        return {"username": club.username, "posts": posts}
    except Exception as error:
        return "error in getting posts"


@posts.route("/club/subscribe", methods=["POST"])
@authenticate
def subscribeClub():
    try:
        data = request.get_json()
        club_username = data["club_username"]
        if club_username:
            subscribe_club(club_username, request.user)
            return "club is subscribed"
        raise Exception("invalid request")
    except Exception as error:
        return "error in subscribing"


@posts.route("/club", methods=["GET"])
@authenticate
def getClubs():
    try:
        user = request.user
        clubs = ClubUserRelationship.select().where(ClubUserRelationship.user == user)
        club_list = []
        for club in clubs:
            club_list.append(club.club.username)
        return {"clubs": club_list}
    except:
        return "error"


def scrape_posts(time_interval=120):
    try:
        query = Club.select()
        for club in query:
            posts = ScrapePost().getPosts(club.username)
            save_posts(posts, club.username)
    except Exception as error:
        raise Exception("error in scraping")
    threading.Timer(time_interval, scrape_posts).start()
