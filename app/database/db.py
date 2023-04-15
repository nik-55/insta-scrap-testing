from .config import database
from app.models.post import Post
from app.models.club import Club
from app.models.user import User
from app.models.club_user_relationship import ClubUserRelationship


def create_tables():
    with database:
        database.create_tables([Post, Club, User, ClubUserRelationship])


def save_posts(posts, username):
    club = Club.get(Club.username == username)
    try:
        if club:
            with database.atomic():
                for post in posts:
                    Post.create(src=post["src"], caption=post["caption"], club=club)
        else:
            raise Exception("club is not subscribed")
    except Exception as error:
        raise Exception("error in saving posts")


def subscribe_club(club_username, user):
    try:
        club = Club.get_or_none(Club.username == club_username)
        if not club:
            club = Club.create(username=club_username)
        ClubUserRelationship.create(user=user, club=club)
        return "subscribed successfully"
    except Exception as error:
        raise Exception("not subscribed")


def save_user(username, password):
    User.create(username=username, password=password)
    return "Register successfully"
