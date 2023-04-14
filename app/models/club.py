from .base_modal import BaseModel
from peewee import CharField


class Club(BaseModel):
    username = CharField(unique=True)
