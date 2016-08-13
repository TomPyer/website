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

    def __init__(self,id,user,text):
        self.id = id
        self.user = user
        self.text = text

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