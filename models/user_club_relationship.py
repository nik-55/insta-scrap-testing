from .base_modal import BaseModel
from peewee import ForeignKeyField
from .user import User
from .club import Club

class Relationship(BaseModel):
    user = ForeignKeyField(User,backref='users')
    club = ForeignKeyField(Club,backref='clubs')

    class Meta:
        indexes = (
            (('user', 'club'), True),
        )