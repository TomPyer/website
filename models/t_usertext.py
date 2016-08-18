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

class Usertext(db.Model):
    __tablename__ = 'Usertext'

    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(80),index=True)
    text = db.Column(db.String(1024),index=True)
    createTime = db.Column(db.DateTime,index=True)

    def __init__(self,user,text,createtime):
        self.user = user
        self.text = text
        self.createTime = createtime

    def __repr__(self):
        return '%s (%r,%r,%r,%r)' %(self.__class__.__name__,self.user,self.text,self.createTime,self.forward)

    def inset(a):
        db.session.add(a)
        db.session.commit()


    def into_sql(sql):
        db.engine.execute(sql)


if __name__ == "__main__":
    db.create_all()