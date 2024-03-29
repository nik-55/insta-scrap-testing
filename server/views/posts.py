from .auth import authenticate
from flask import Blueprint, request
from server.models.club import Club
from server.models.club_user_relationship import ClubUserRelationship
from server.database.db import save_posts_from_multiple_clubs, subscribe_club

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


@posts.route("/all_clubs", methods=["GET"])
def _():
    clubs = Club.select()
    club_list = []
    for club in clubs:
        club_list.append(club.username)
    return {"clubs": club_list}


@posts.route("/all_clubs_update", methods=["POST"])
def _i():
    data = request.get_json()
    txt = save_posts_from_multiple_clubs(data["clubs_info"])
    return txt
