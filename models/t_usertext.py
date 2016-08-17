# coding:utf-8
#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wobuzhidaoA123.@localhost:3306/flask_work'
db = SQLAlchemy(app)

class usertext(object):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(80),unique=True)
    text = db.Column(db.String(1024),unique=True)
    createTime = db.Column(db.DateTime,unique=True)
    forward = db.Column(db.Integer,unique=True)
    forwardUser = db.Column(db.String(1024),unique=True)
    comment = db.Column(db.Integer,unique=True)
    commentUser = db.Column(db.String(1024),unique=True)
    likes = db.Column(db.Integer,unique=True)
    likesUser = db.Column(db.String(1024),unique=True)
    collection = db.Column(db.Integer,unique=True)
    collectionUser = db.Column(db.String(1024),unique=True)
    topFlag = db.Column(db.Integer,unique=True)

    def __init__(self,id,user,text,createtime,forward,forwarduser,comment,commentuser,likes,likesuser,collection,collectionuser,topflag):
        self.id = id
        self.user = user
        self.text = text
        self.createTime = createtime
        self.forward = forward
        self.forwardUser = forwarduser
        self.comment = comment
        self.commentUser = commentuser
        self.likes = likes
        self.likesUser = likesuser
        self.collection = collection
        self.collectionUser = collectionuser
        self.topFlag = topflag

    def add(self):
        pass

    def remove(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

if __name__ == "__main__":
    db.create_all()