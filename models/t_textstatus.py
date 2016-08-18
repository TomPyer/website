# coding:utf-8
#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.t_usertext import Usertext

import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wobuzhidaoA123.@localhost:3306/flask_work'
db = SQLAlchemy(app)


class TextStatus(db.Model):
    __tablename__ = 'TextStatus'
    id = db.Column(db.Integer,primary_key=True)
    textcode = db.Column(db.String(100),index=True)
    forward = db.Column(db.Integer,index=True)
    forwardUser = db.Column(db.String(1024),index=True)
    comment = db.Column(db.Integer,index=True)
    commentUser = db.Column(db.String(1024),index=True)
    likes = db.Column(db.Integer,index=True)
    likesUser = db.Column(db.String(1024),index=True)
    collection = db.Column(db.Integer,index=True)
    collectionUser = db.Column(db.String(1024),index=True)


    def __init__(self,textcode,forward,forwardUser,comment,commentUser,likes,likesUser,collection,collectionUser):
        self.textcode = textcode
        self.forward = forward
        self.forwardUser = forwardUser
        self.comment = comment
        self.commentUser = commentUser
        self.likes = likes
        self.likesUser = likesUser
        self.collection = collection
        self.collectionUser = collectionUser


    def __repr__(self):
        return self.__class__.__name__


    def inset(a):
        db.session.add(a)
        db.session.commit()
        return 'yes'

    def into_sql(sql):
        db.engine.execute(sql)
        return 'yes'

if __name__ == "__main__":
    db.create_all()