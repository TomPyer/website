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

class User(db.Model):
    __tablename__ = 'User'

    id =  db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),index=True)
    password = db.Column(db.String(80),index=True)
    email = db.Column(db.String(320),index=True)
    phone = db.Column(db.String(32),index=True)

    def __init__(self,username,password,email,phone):
        self.username =username
        self.password =password
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '%s (%r,%r,%r,%r)' %(self.__class__.__name__,self.username,self.password,self.email,self.phone)

    def inset(a):
        db.session.add(a)
        db.session.commit()
        return 'OK!'

if __name__ == '__main__':
    db.create_all()
