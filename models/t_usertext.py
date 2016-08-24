# coding:utf-8
#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wobuzhidaoA123.@localhost:3306/flask_work'
db = SQLAlchemy(app)

class Usertext(db.Model):
    __tablename__ = 'Usertext'

    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(80),index=True)
    text = db.Column(db.String(1024),index=True)
    createTime = db.Column(db.DateTime,index=True)
    textcode = db.Column(db.String(100),index=True)
    forward = db.Column(db.Integer,index=True)
    forwardUser = db.Column(db.String(1024),index=True)
    comment = db.Column(db.Integer,index=True)
    commentUser = db.Column(db.String(1024),index=True)
    likes = db.Column(db.Integer,index=True)
    likesUser = db.Column(db.String(1024),index=True)
    collection = db.Column(db.Integer,index=True)
    collectionUser = db.Column(db.String(1024),index=True)

    '''
    def __init__(self,user,text,createtime,textcode,forward,forwardUser,comment,commentUser,likes,likesUser,collection,collectionUser):
        self.user = user
        self.text = text
        self.createTime = createtime
        self.textcode = textcode
        self.forward = forward
        self.forwardUser = forwardUser
        self.comment = comment
        self.commentUser = commentUser
        self.likes = likes
        self.likesUser = likesUser
        self.collection = collection
        self.collectionUser = collectionUser '''

    def __repr__(self):
        return '%s (%r,%r,%r)' %(self.__class__.__name__,self.user,self.text,self.createTime)

    def inset(self,user,text,createtime):
        a = Usertext(user=user,text=text,createTime=createtime,textcode='',forward=0,forwardUser='',comment=0,commentUser='',likes=0,likesUser='',collection=0,collectionUser='')
        db.session.add(a)
        db.session.commit()
        return 'yes'

    def commit(self):
        db.session.commit()
        return 'yes'

    def into_sql(sql):
        db.engine.execute(sql)
        return 'yes'

if __name__ == "__main__":
    db.create_all()