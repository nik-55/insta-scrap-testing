from .base_modal import BaseModel
from peewee import CharField

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
