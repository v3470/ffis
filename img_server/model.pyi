from .db import db
from flask import Flask
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column,Integer,DateTime,String

class Image(db.Model):
    query:BaseQuery
    id:Column[Integer]
    path:Column[String]
    old_name:Column[String]
    time:Column[DateTime]
    count:Column[Integer]
    def __init__(self,path,old_name=...):
    @classmethod
    def get(cls,path)->Image:...
    @classmethod
    def get_next_path(cls)->str: ...


class NextKey(db.Model):
    query:BaseQuery
    id:Column[Integer]
    key:Column[String]
    value:Column[String]

    @classmethod
    def get(cls,key:str)->NextKey:...

    @classmethod
    def update(cls):...


def init_key()->None: ...
def init_key_dir(app:Flask)->None: ...


