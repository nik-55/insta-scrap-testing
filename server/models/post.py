from .base_modal import BaseModel
from peewee import CharField, ForeignKeyField
from .club import Club


class Post(BaseModel):
    caption = CharField()
    src = CharField()
    club = ForeignKeyField(Club, backref="posts")
