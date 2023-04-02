from .config import database
from .models.post import Post
from .models.club import Club

def create_tables():
    with database:
        database.create_tables([Post,Club])

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
